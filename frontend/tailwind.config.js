/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    'node_modules/flowbite-react/**/*.{js,jsx,ts,tsx',

  ],
  theme: {
    extend: {
      colors: {
        "primary": "#141414",
        "blue": "#3B82F6",
        "purple": "#8A3FFC", // Example of adding a new color
        "white": "#fff",
        "pink": "#FFC0CB",
      }
    },
  },
  plugins: [require('flowbite/plugin')],
}

