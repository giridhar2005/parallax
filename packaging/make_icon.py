#!/usr/bin/env python3
"""Programmatic App Icon Generator for Parallax.

Renders a minimalist, dark-mode 1024x1024 geometric icon featuring an interlocking
split-frame forensic crosshair (#FAFAFA and #EF4444 on #09090B canvas) and compiles
it into a native macOS Parallax.icns via iconutil.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw


def create_base_icon(size: int = 1024) -> Image.Image:
    """Render the 1024x1024 high-resolution master icon."""
    img = Image.new("RGBA", (size, size), (9, 9, 11, 255))  # #09090B canvas
    draw = ImageDraw.Draw(img)

    margin = int(size * 0.08)
    corner_radius = int(size * 0.22)

    # 1. Outer macOS Squircle Container
    squircle_rect = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(
        squircle_rect,
        radius=corner_radius,
        fill=(17, 17, 19, 255),       # #111113 panel surface
        outline=(39, 39, 42, 255),    # #27272A hairline border
        width=int(size * 0.008),
    )

    center_x = size // 2
    center_y = size // 2
    target_radius = int(size * 0.28)
    line_thickness = max(4, int(size * 0.016))

    # 2. Concentric Forensic Target Rings
    draw.ellipse(
        [center_x - target_radius, center_y - target_radius, center_x + target_radius, center_y + target_radius],
        outline=(63, 63, 70, 255),   # #3F3F46 inner ring
        width=int(size * 0.006),
    )

    inner_radius = int(target_radius * 0.55)
    draw.ellipse(
        [center_x - inner_radius, center_y - inner_radius, center_x + inner_radius, center_y + inner_radius],
        outline=(239, 68, 68, 120),  # Transparent crimson
        width=int(size * 0.005),
    )

    # 3. Interlocking Split-Frame Crosshair
    # Left Half: Forensic Claim Stream (White #FAFAFA)
    left_line = [center_x - target_radius - int(size * 0.06), center_y, center_x - int(size * 0.04), center_y]
    draw.line(left_line, fill=(250, 250, 250, 255), width=line_thickness)

    top_line = [center_x, center_y - target_radius - int(size * 0.06), center_x, center_y - int(size * 0.04)]
    draw.line(top_line, fill=(250, 250, 250, 255), width=line_thickness)

    # Right Half: Contradiction Breach (Crimson #EF4444)
    right_line = [center_x + int(size * 0.04), center_y, center_x + target_radius + int(size * 0.06), center_y]
    draw.line(right_line, fill=(239, 68, 68, 255), width=line_thickness)

    bottom_line = [center_x, center_y + int(size * 0.04), center_x, center_y + target_radius + int(size * 0.06)]
    draw.line(bottom_line, fill=(239, 68, 68, 255), width=line_thickness)

    # 4. Center Laser Point
    core_dot = int(size * 0.02)
    draw.ellipse(
        [center_x - core_dot, center_y - core_dot, center_x + core_dot, center_y + core_dot],
        fill=(239, 68, 68, 255),
    )

    return img


def generate_icns(output_path: Path) -> Path:
    """Generate macOS .icns multi-resolution icon bundle using native iconutil."""
    packaging_dir = output_path.parent
    iconset_dir = packaging_dir / "Parallax.iconset"
    iconset_dir.mkdir(parents=True, exist_ok=True)

    master = create_base_icon(1024)
    master.save(packaging_dir / "icon.png")

    # Standard macOS icon resolutions
    icon_specs = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for filename, s in icon_specs:
        resized = master.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(iconset_dir / filename)

    # Compile with macOS iconutil if available
    if shutil.which("iconutil"):
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(output_path)],
            check=True,
        )
        shutil.rmtree(iconset_dir, ignore_errors=True)
        print(f"Compiled macOS icon bundle: {output_path}")
    else:
        print("iconutil not found; keeping PNG icon assets.")

    return output_path


def main():
    target_icns = Path(__file__).resolve().parent / "Parallax.icns"
    generate_icns(target_icns)


if __name__ == "__main__":
    main()
