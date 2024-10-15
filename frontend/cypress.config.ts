import {defineConfig} from 'cypress';
import {faker} from '@faker-js/faker';

export default defineConfig({
  e2e: {
    testIsolation: false,
    chromeWebSecurity: false,
    experimentalModifyObstructiveThirdPartyCode: true,
    baseUrl: 'http://localhost:4200',
    fixturesFolder: 'cypress/fixtures',
    screenshotsFolder: 'cypress/screenshots',
    supportFile: 'cypress/support/e2e.ts',
    videosFolder: 'cypress/videos',
    video: true,
    defaultCommandTimeout: 60000,
    viewportHeight: 768,
    viewportWidth: 1440,
    waitForAnimations: true,
    includeShadowDom: false,
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
      TEST_RUN_UUID: crypto.randomUUID(),
      TEST_RUN_UNIQUE_STRING: faker.helpers.multiple(faker.word.noun, {count: 3}).join(''),
    },
  },
});
