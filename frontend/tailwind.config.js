/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Barclays-inspired palette
        primary: '#00AEEF',
        'primary-dark': '#0077B6',
        danger: '#F44336',
        warning: '#FF9800',
        success: '#4CAF50',
      },
    },
  },
  plugins: [],
};
