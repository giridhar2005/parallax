/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#09090B",
        panel: "#111113",
        panelElevated: "#18181B",
        hairline: "#27272A",
        hairlineLight: "#3F3F46",
        crimson: "#EF4444",
        amberForensic: "#F59E0B",
        emeraldForensic: "#10B981",
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "Courier New", "monospace"],
      },
    },
  },
  plugins: [],
};
