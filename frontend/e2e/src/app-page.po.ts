import {
  browser,
  by,
  element,
  ElementArrayFinder,
  ElementFinder,
  ExpectedConditions,
} from 'protractor';
import { protractor } from 'protractor/built/ptor';


export class AppPage {

  constructor() {
    this.maximize();
  }

  maximize() {
    return browser.driver.manage().window().maximize();
  }

  resizeTo(width: number, height: number) {
    return browser.driver.manage().window().setSize(width, height);
  }

  waitFor(t: number) {
    return browser.sleep(t);
    // Might need to enable this if Webdriver gets disconnected from DOM
    // browser.waitForAngularEnabled(false);
  }

  waitForAngularEnabled(enabled: boolean) {
    return browser.waitForAngularEnabled(enabled);
  }

  waitForText(selector: string, text: string) {
    const e = this.getElement(selector);
    return browser.wait(ExpectedConditions.textToBePresentInElement(e, text), 5000);
  }

  waitForAnimations() {
    return browser.sleep(3000);
    // Might need to enable this if Webdriver gets disconnected from DOM
    // browser.waitForAngularEnabled(false);
  }

  waitForStale(selector: string) {
    const e = this.getElement(selector);
    return browser.wait(ExpectedConditions.stalenessOf(e), 5000);
  }

  waitForClickable(selector: string) {
    const e = this.getElement(selector);
    return browser.wait(ExpectedConditions.elementToBeClickable(e), 5000);
  }

  waitForNotVisible(selector: string) {
    const e = this.getElement(selector);
    return browser.wait(ExpectedConditions.invisibilityOf(e), 5000);
  }

  // If given CSS selector is found on the page, waits 5 seconds for the element to become visible. If it's not found
  // on the page, recursively calls itself maxLoops number of times, waiting 1 second between each call, until the
  // element becomes present.
  async waitForVisible(selector: string, maxLoops = 5) {
    const numElements = await this.getElements(selector).count();
    if (numElements > 0) {
      const e = await this.getElement(selector);
      return browser.wait(
        ExpectedConditions.visibilityOf(e),
        5000,
        `Element "${selector}" is still not visible after waiting for 5 seconds.`
      );
    } else if (maxLoops > 0) {
      await this.waitFor(1000);
      await this.waitForVisible(selector, maxLoops - 1);
    } else {
      expect(numElements).toBeGreaterThan(0, `Element "${selector}" is not present on the page.`);
    }
  }

  getLocalStorageVar(name: string) {
    return browser.executeScript(`return window.localStorage.getItem('${name}');`);
  }

  getSessionStorageVar(key: string) {
    return browser.executeScript(`return window.sessionStorage.getItem('${key}');`);
  }

  async clickLinkTo(route: string) {
    const selector = `[href="#${route}"]`;
    this.waitForClickable(selector);
    this.clickElement(selector);
    const actualRoute = await this.getRoute();
    expect(actualRoute).toEqual(route);
  }

  async clickLinkToVariation(route: string) {
    const selector = `[href="#${route}"]`;
    this.waitForClickable(selector);
    this.clickElement(selector);
    const actualRoute = await this.getRoute();
    const routeLength = route.length;
    expect(actualRoute.substr(0, routeLength)).toEqual(route);
  }

  getParagraphText() {
    return this.getElement('app-root h1').getText();
  }

  clickElement(selector: string) {
    this.waitForClickable(selector);
    this.scrollTo(selector);
    this.focus(selector);
    return this.getElement(selector).click();
  }

  clickDropdownItem(dropdownSelector: string, nthItem: number) {
    const optionSelector = `mat-option:nth-of-type(${nthItem})`;
    this.waitForVisible(dropdownSelector);
    this.clickElement(dropdownSelector);
    this.waitForVisible(optionSelector);
    this.clickElement(optionSelector);
    this.waitForNotVisible(optionSelector);
  }

  async isVisible(selector: string) {
    const numElements = await this.getElements(selector).count();
    return (numElements > 0) ? this.getElement(selector).isDisplayed() : false;
  }

  getElement(selector: string): ElementFinder {
    return element.all(by.css(selector)).first();
  }

  getElements(selector: string): ElementArrayFinder {
    return element.all(by.css(selector));
  }

  getChildElement(selector: string, parentElement: ElementFinder) {
    return parentElement.element(by.css(selector));
  }

  getChildElements(selector: string, parentElement: ElementArrayFinder) {
    return parentElement.all(by.css(selector));
  }

  getUrl() {
    return browser.getCurrentUrl();
  }

  async getRoute() {
    const url = await this.getUrl();
    return url.split('#')[1];
  }

  pressKey(keyCode: string) {
    browser.actions().sendKeys(protractor.Key[keyCode]).perform();
  }

  focus(selector: string) {
    return browser.controlFlow().execute(() => {
      return browser.executeScript('arguments[0].focus()', this.getElement(selector).getWebElement());
    });
  }

  async isFocused(selector: string) {
    const expectedEl = await this.getElement(selector);
    const expectedId = await expectedEl.getAttribute('id');
    const actualEl = await browser.switchTo().activeElement();
    const actualId = await actualEl.getAttribute('id');
    return expectedId === actualId;
  }

  inputText(selector: string, textToEnter: string, clearFirst?: boolean) {
    expect(this.getElements(selector).count()).toEqual(1);
    const field = this.getElement(selector);

    if (clearFirst) {
      field.clear();
      expect(field.getAttribute('value')).toEqual('');
    }

    field.sendKeys(textToEnter);
    expect(field.getAttribute('value')).toEqual(textToEnter);
  }

  navigateToUrl(url: string) {
    return browser.get(url);
  }

  navigateToHome() {
    return browser.get('/');
  }

  refresh() {
    return browser.refresh();
  }

  clickAndExpectRoute(clickSelector: string, expectedRoute: string | RegExp) {
    this.waitForClickable(clickSelector);
    this.clickElement(clickSelector);
    if (typeof expectedRoute === 'string') {
      expect(this.getRoute()).toEqual(expectedRoute);
    } else {
      expect(this.getRoute()).toMatch(expectedRoute);
    }
  }

  getRandomString(length: number) {
    const s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    return Array(length).join().split(',').map(() => s.charAt(Math.floor(Math.random() * s.length))).join('');
  }

  getRandomNumString(length: number) {
    const s = '123456789';
    return Array(length).join().split(',').map(() => s.charAt(Math.floor(Math.random() * s.length))).join('');
  }

  getRandomDate(start: Date, end: Date): Date {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
  }

  scrollTo(selector: string) {
    browser.controlFlow().execute(() => {
      browser.executeScript('arguments[0].scrollIntoView(false)', this.getElement(selector).getWebElement());
    });
  }

  tabThroughAllFields() {
    this.focus('formly-form');

    const selector = '' +
      'formly-field [id*="_input_"],' +
      'formly-field [id*="_datepicker_"],' +
      'formly-field [id*="_radio_"],' +
      'formly-field [id*="_checkbox_"],' +
      'formly-field [id*="_select_"]';

    this.getElements(selector).each(_ => this.pressKey('TAB'));
  }

  async fillOutFields(selector: string) {
    const elements: ElementFinder[] = await this.getElements(selector);

    for (const e of elements) {
      const id = await e.getAttribute('id');
      if (id) {
        this.scrollTo(`#${id}`);

        if (/_input_email_/.test(id)) {
          const email = this.getRandomString(8) + '@whatever.com';
          e.sendKeys(email);
        } else if (/_input_phone_/.test(id)) {
          const phone = this.getRandomNumString(10);
          e.sendKeys(phone);
        } else if (/_input_zip_/.test(id)) {
          const zip = this.getRandomNumString(5);
          e.sendKeys(zip);
        } else if (/_input_/.test(id)) {
          e.getAttribute('type').then(eType => {
            let str = '';

            if (eType === 'number') {
              str = this.getRandomNumString(2);
            } else {
              str = this.getRandomString(16);
            }
            e.sendKeys(str);
          });
        } else if (/_datepicker_/.test(id)) {
          const date = this.getRandomDate(new Date(2000, 0, 1), new Date());
          const mm = date.getMonth() + 1;
          const dd = date.getDate();
          const yyyy = date.getFullYear();
          const dateStr = `${mm}/${dd}/${yyyy}`;
          e.clear();
          e.sendKeys(dateStr);
        } else if (/_radio_/.test(id)) {
          e.$(`#${id}_0 .mat-radio-container`).click();
        } else if (/_checkbox_/.test(id)) {
          e.$(`#${id}_0`).click();
        } else if (/_select_/.test(id)) {
          e.click();
          const optionSelector = 'mat-option:first-of-type';
          await this.waitForVisible(optionSelector);
          await this.getElement(optionSelector).click();
          await this.waitForNotVisible(optionSelector);
        }
      }
    }

    const multicheckboxSelector = `${selector} formly-field-mat-multicheckbox mat-checkbox:first-of-type`;
    const numCheckboxes = await this.getElements(multicheckboxSelector).count();
    if (numCheckboxes > 0) {
      this.getElements(`${multicheckboxSelector} .mat-checkbox-inner-container`).each(c => {
        c.click();
      });
    }
  }
}
