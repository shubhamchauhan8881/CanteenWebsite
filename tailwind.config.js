/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        Canteen: '#004B93',
      }
    },
  },
  plugins: [require('daisyui'),],
}

