import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        terminal: {
          bg: "#0b0f14",
          panel: "#101820",
          line: "#263241",
          text: "#e6edf3",
          muted: "#9aa7b5",
          safe: "#45c486",
          warn: "#e8b84a",
          risk: "#f06a6a",
          action: "#5aa7ff"
        }
      }
    }
  },
  plugins: []
} satisfies Config;
