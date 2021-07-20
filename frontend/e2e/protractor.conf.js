// Protractor configuration file, see link for more information
// https://github.com/angular/protractor/blob/master/lib/config.ts

const { SpecReporter, StacktraceOption } = require('jasmine-spec-reporter');
process.env.CHROME_BIN = require('puppeteer').executablePath()

exports.config = {
  allScriptsTimeout: 30000,
  specs: [
    './src/*.e2e-spec.ts'
  ],
  capabilities: {
    chromeOptions: {
      args: [
        '--disable-gpu',
        '--window-size=1440, 900',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--dev-server-target=',
      ],
      binary: process.env.CHROME_BIN
    },
    browserName: 'chrome',
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
    jasmine.getEnv().addReporter(new SpecReporter({ spec: { displayStacktrace: StacktraceOption.PRETTY } }));
  },
};
