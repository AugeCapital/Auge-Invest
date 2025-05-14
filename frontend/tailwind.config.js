/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}", // If using App Router
  ],
  darkMode: 'class', // or 'media' or 'selector'
  theme: {
    extend: {
      colors: {
        // Example colors, to be replaced by STYLE_GUIDE.md definitions
        'auge-blue': '#0052CC',
        'auge-green': '#00875A',
        'auge-dark-bg': '#0D1117',
        'auge-dark-card': '#161B22',
        'auge-light-text': '#172B4D',
        'auge-dark-text': '#C9D1D9',
      },
      fontFamily: {
        // Example fonts, to be replaced by STYLE_GUIDE.md definitions
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

