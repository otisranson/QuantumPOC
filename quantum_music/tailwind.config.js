/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#f2ecdd',
        'paper-dark': '#e7dcc0',
        ink: '#1f2b3a',
        'ink-soft': '#42566c',
        brass: '#b5842a',
        'brass-light': '#d9ac52',
        verdigris: '#3e6b63',
        rose: '#a13f4c',
      },
      fontFamily: {
        display: ['"Spectral"', 'Georgia', 'ui-serif', 'serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      boxShadow: {
        key: '0 5px 0 rgba(31,43,58,0.35)',
        'key-black': '0 4px 0 rgba(0,0,0,0.5)',
      },
      backgroundImage: {
        grain: "radial-gradient(rgba(31,43,58,0.05) 1px, transparent 1px)",
      },
      backgroundSize: {
        'grain-fine': '4px 4px',
      },
    },
  },
  plugins: [],
};
