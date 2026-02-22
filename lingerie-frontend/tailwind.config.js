/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        noir: '#0a0a0a',
        charcoal: '#1a1a1a',
        gold: '#c9a96e',
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
      }
    },
  },
  plugins: [],
}
