import {defineConfig} from 'cypress';

export default defineConfig({
  e2e: {
    testIsolation: false,
    chromeWebSecurity: false,
    experimentalModifyObstructiveThirdPartyCode: true,
    baseUrl: 'http://localhost:4200',
    fixturesFolder: 'cypress/fixtures',
    screenshotsFolder: 'cypress/screenshots',
    video: true,
    supportFile: 'cypress/support/e2e.ts',
    videosFolder: 'cypress/videos',
    defaultCommandTimeout: 30000,
    viewportHeight: 900,
    viewportWidth: 1440,
    waitForAnimations: true,
    setupNodeEvents(on, config) {
      require('cypress-terminal-report/src/installLogsPrinter')(on, {
        printLogsToConsole: 'always',
      });

      require('cypress-fail-fast/plugin')(on, config);

      return config;
    },
    env: {
      FAIL_FAST_STRATEGY: 'run',
      FAIL_FAST_PLUGIN: true,
      FAIL_FAST_ENABLED: true,
      FAIL_FAST_BAIL: 1,
    },
  },
});
