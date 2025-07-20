module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#a29bfe',
        'primary-dark': '#8c7ae6',
        'primary-light': '#b8a9ff',
        secondary: '#fab1a0',
        'secondary-dark': '#f39c7d',
        'secondary-light': '#ffc4b3',
        background: '#1e1e2f',
        'bg-primary': '#1e1e2f',
        'bg-secondary': '#2c2c44',
        'bg-tertiary': '#4a4a6a',
        foreground: '#e0e0e0',
        muted: '#b8b8b8',
        error: '#e17055',
        info: '#74b9ff',
        success: '#00b894',
        warning: '#fdcb6e',
        border: '#4a4a6a',
        'border-light': '#2c2c44',
        'text-primary': '#e0e0e0',
        'text-secondary': '#b8b8b8',
        'text-muted': '#8a8a8a',
      },
      fontFamily: {
        heading: ['MedievalSharp', 'cursive'],
        serif: ['Lora', 'serif'],
        body: ['Lora', 'serif'],
        fallback: [
          '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen',
          'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', 'sans-serif'
        ],
      },
    },
  },
  plugins: [],
} 