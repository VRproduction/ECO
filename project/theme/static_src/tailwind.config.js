/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
      // Templates within theme app (e.g. base.html)
      '../templates/**/*.html',
      // Templates in other apps
      '../../templates/**/*.html',
      // Ignore files in node_modules
      '!../../**/node_modules',
      // Include JavaScript files that might contain Tailwind CSS classes
      '../../**/*.js',
      // Include Python files that might contain Tailwind CSS classes
      '../../**/*.py'
  ],
    theme: {
        extend: {
          colors: {
            first: '#039D2E', // Ana renk
            'first-hover': '#028C1F', // Ana renk hover
            second: '#ffed4a', // İkincil renk
            'second-hover': '#fcd34d', // İkincil renk hover
            accent: '#e3342f', // Vurgu rengi
            'accent-hover': '#c53030', // Vurgu rengi hover
            background: '#f8fafc', // Arka plan rengi
            textColor: '#253D4E', // Metin rengi
          },
        },
      },      
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
