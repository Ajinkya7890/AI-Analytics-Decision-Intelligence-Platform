/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: '#101014',
          sidebar: '#0C0C10',
          card: '#18181F',
          surface: '#1F1F27',
          hover: '#242430',
        },
        border: {
          DEFAULT: '#2A2A35',
          subtle: '#22222C',
          active: '#3A3A4A',
        },
        accent: {
          DEFAULT: '#8B7CFF',
          hover: '#7A6AE6',
          muted: 'rgba(139, 124, 255, 0.12)',
          border: 'rgba(139, 124, 255, 0.35)',
        },
        content: {
          primary: '#F4F4F6',
          secondary: '#9E9EA8',
          muted: '#6C6C78',
        },
        status: {
          success: '#34D399',
          'success-bg': 'rgba(52, 211, 153, 0.12)',
          warning: '#FBBF24',
          'warning-bg': 'rgba(251, 191, 36, 0.12)',
          error: '#F87171',
          'error-bg': 'rgba(248, 113, 113, 0.12)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Menlo', 'monospace'],
      },
      boxShadow: {
        'panel': '0 4px 20px -2px rgba(0, 0, 0, 0.45)',
        'elevated': '0 10px 30px -5px rgba(0, 0, 0, 0.65)',
      }
    },
  },
  plugins: [],
};
