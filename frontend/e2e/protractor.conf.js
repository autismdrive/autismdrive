// Protractor configuration file, see link for more information
// https://github.com/angular/protractor/blob/master/lib/config.ts

const { SpecReporter } = require('jasmine-spec-reporter');

exports.config = {
  allScriptsTimeout: 30000,
  specs: [
    './src/*.e2e-spec.ts'
  ],
  capabilities: {
    chromeOptions: {
      args: [
        "--window-size=1440x900",
        // "--headless",
        // "--no-sandbox",
      ]
    },
    'browserName': 'chrome'
  },
  directConnect: true,
  baseUrl: 'http://localhost:4200/',
  framework: 'jasmine',
  jasmineNodeOpts: {
    showColors: true,
    defaultTimeoutInterval: 30000,
    print: function() { }
  },
  onPrepare() {
    require('ts-node').register({
      project: './tsconfig.e2e.json'
    });
    jasmine.getEnv().addReporter(new SpecReporter({ spec: { displayStacktrace: true } }));
  }
};
