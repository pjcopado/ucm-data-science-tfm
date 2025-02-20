module.exports = {
  extends: [
    'plugin:react/recommended',        // Reglas recomendadas para React
    'plugin:react-hooks/recommended',   // Reglas recomendadas para React Hooks
    'eslint:recommended',               // Reglas básicas recomendadas de ESLint
  ],
  plugins: ['react', 'react-hooks'],    // Asegúrate de que react-hooks está en los plugins
  rules: {
    'react-hooks/exhaustive-deps': 'warn',  // Activa la regla para exhaustivas dependencias
  },
  settings: {
    react: {
      version: 'detect',               // Asegúrate de que ESLint detecte la versión de React
    },
  },
};
