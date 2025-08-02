module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Основные цвета - теплые оттенки
        primary: '#8B4513', // Saddle Brown - теплый коричневый
        'primary-dark': '#654321', // Dark Brown
        'primary-light': '#A0522D', // Sienna
        
        // Вторичные цвета - золотистые оттенки
        secondary: '#DAA520', // Goldenrod
        'secondary-dark': '#B8860B', // Dark Goldenrod
        'secondary-light': '#F4A460', // Sandy Brown
        
        // Акцентные цвета
        accent: '#CD853F', // Peru - теплый оранжево-коричневый
        'accent-dark': '#A0522D', // Sienna
        'accent-light': '#DEB887', // Burlywood
        
        // Фоновые цвета - мягкие светлые оттенки
        background: '#FDF6E3', // Warm cream
        'bg-primary': '#FDF6E3', // Warm cream
        'bg-secondary': '#F5F5DC', // Beige
        'bg-tertiary': '#FAF0E6', // Linen
        
        // Текстовые цвета - темные, но не слишком резкие
        foreground: '#2F2F2F', // Soft black
        muted: '#6B6B6B', // Medium gray
        'text-primary': '#2F2F2F', // Soft black
        'text-secondary': '#4A4A4A', // Dark gray
        'text-muted': '#6B6B6B', // Medium gray
        
        // Статусные цвета - приглушенные
        error: '#D2691E', // Chocolate - теплый красный
        info: '#4682B4', // Steel Blue
        success: '#228B22', // Forest Green
        warning: '#DAA520', // Goldenrod
        
        // Границы - мягкие оттенки
        border: '#D2B48C', // Tan
        'border-light': '#F5DEB3', // Wheat
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