/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        clinical: {
          50: '#f0f7ff',
          100: '#e0effe',
          500: '#0056D2',
          600: '#0043a8',
          700: '#003482',
        },
        mint: {
          50: '#e6f7f2',
          500: '#00A878',
          600: '#00855f',
        },
        risk: {
          excellent: '#00A878',
          good: '#10B981',
          moderate: '#F59E0B',
          poor: '#EF4444',
          grey: '#64748B',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
