/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#1683F5',
          navy: '#102A56',
          lightBlue: '#F0F7FF',
        }
      }
    },
  },
  plugins: [],
}
