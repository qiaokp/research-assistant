/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'claude-orange': '#f97316',
        'claude-bg': '#1a1a1a',
        'claude-surface': '#2d2d2d',
        'claude-border': '#404040',
      },
    },
  },
  plugins: [],
}
