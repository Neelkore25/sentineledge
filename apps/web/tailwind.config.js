/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        editorial: {
          bg: 'var(--bg-primary)',
          surface: 'var(--bg-surface)',
          panel: 'var(--bg-panel)',
          border: 'var(--border-color)',
          text: 'var(--text-primary)',
          muted: 'var(--text-muted)',
          accent: 'var(--accent-signal)',
          accentMuted: 'var(--accent-muted)',
        },
        status: {
          healthy: '#10B981',
          warning: '#F59E0B',
          critical: '#EF4444',
          info: '#3B82F6',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'IBM Plex Mono', 'monospace'],
      }
    },
  },
  plugins: [],
};
