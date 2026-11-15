#!/usr/bin/env bash
# ==============================================================================
# Parallax macOS .app & .dmg Build Pipeline (Apple Silicon arm64)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> [1/5] Generating multi-resolution icon bundle..."
cd "$ROOT_DIR"
uv run python packaging/make_icon.py

echo "==> [2/5] Building React TypeScript production distribution..."
cd "$ROOT_DIR/frontend"
npm run build

echo "==> [3/5] Running PyInstaller bundle compilation (arm64)..."
cd "$ROOT_DIR"
uv run pyinstaller --clean -y packaging/Parallax.spec

echo "==> [4/5] Packaging drag-to-Applications macOS DMG installer..."
RELEASE_DIR="$ROOT_DIR/release"
mkdir -p "$RELEASE_DIR"
DMG_NAME="Parallax-v1.0.0-macOS-arm64.dmg"
DMG_PATH="$RELEASE_DIR/$DMG_NAME"
STAGING_DIR="$ROOT_DIR/dist/dmg_staging"

rm -rf "$STAGING_DIR" "$DMG_PATH"
mkdir -p "$STAGING_DIR"

# Stage Parallax.app and drag-to-Applications symlink
cp -R "$ROOT_DIR/dist/Parallax.app" "$STAGING_DIR/"
ln -s /Applications "$STAGING_DIR/Applications"

if command -v create-dmg >/dev/null 2>&1; then
    echo "Using create-dmg for styled installer window..."
    create-dmg \
        --volname "Parallax" \
        --volicon "$ROOT_DIR/packaging/Parallax.icns" \
        --window-pos 200 120 \
        --window-size 660 400 \
        --icon-size 128 \
        --icon "Parallax.app" 180 190 \
        --app-drop-link 480 190 \
        --hide-extension "Parallax.app" \
        --no-internet-enable \
        "$DMG_PATH" \
        "$STAGING_DIR" || {
            echo "create-dmg exited with warning; falling back to hdiutil..."
            hdiutil create -volname "Parallax" -srcfolder "$STAGING_DIR" -ov -format UDZO "$DMG_PATH"
        }
else
    echo "create-dmg not found; packaging with native macOS hdiutil UDZO..."
    hdiutil create -volname "Parallax" -srcfolder "$STAGING_DIR" -ov -format UDZO "$DMG_PATH"
fi

rm -rf "$STAGING_DIR"

echo "==> [5/5] Generating cryptographic verification checksums..."
cd "$RELEASE_DIR"
shasum -a 256 "$DMG_NAME" > SHA256SUMS.txt

echo "=============================================================================="
echo " Parallax Build Successful!"
echo " Application Bundle: $ROOT_DIR/dist/Parallax.app"
echo " Disk Image (.dmg):  $DMG_PATH"
echo " Checksum:           $(cat "$RELEASE_DIR/SHA256SUMS.txt")"
echo "=============================================================================="
