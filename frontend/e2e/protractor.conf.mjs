// Protractor configuration file, see link for more information
// https://github.com/angular/protractor/blob/master/lib/config.ts

import { SpecReporter, StacktraceOption } from "jasmine-spec-reporter";
const seleniumConfig = require("webdriver-manager/selenium/update-config.json");

import * as puppeteer from "puppeteer";
process.env.CHROME_BIN = puppeteer.executablePath();

const browser = await puppeteer.launch()
const version = await browser.version();
const chromeVersion = version.split("/")[1];
await browser.close();

console.log(`Puppeteer Chrome version: ${chromeVersion}`);
console.log(`Selenium Chrome version: ${seleniumConfig.chrome.last}`);

exports.config = {
  allScriptsTimeout: 30000,
  specs: ["./src/*.e2e-spec.ts"],
  capabilities: {
    chromeOptions: {
      args: [
        "--headless",
        "--disable-gpu",
        "--window-size=1440, 900",
        "--dev-server-target=",
        "--remote-debugging-port=4444",
      ],
      binary: process.env.CHROME_BIN,
    },
    browserName: "chrome",
  },
  directConnect: true,
  baseUrl: "http://localhost:4200/",
  framework: "jasmine",
  jasmineNodeOpts: {
    showColors: true,
    defaultTimeoutInterval: 30000,
    print: function () {},
  },
  onPrepare() {
    require("ts-node").register({
      project: "./tsconfig.e2e.json",
    });
    jasmine.getEnv().addReporter(
      new SpecReporter({
        spec: { displayStacktrace: StacktraceOption.PRETTY },
      })
    );
  },
};
