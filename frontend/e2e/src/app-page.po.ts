import { browser, by, element, ExpectedConditions } from 'protractor';

export class AppPage {

  waitForAnimations() {
    browser.sleep(3000);
  }

  waitForStale(selector: string) {
    const e = this.getElement(selector);
    browser.wait(ExpectedConditions.stalenessOf(e), 5000);
  }

  waitForClickable(selector: string) {
    const e = this.getElement(selector);
    browser.wait(ExpectedConditions.elementToBeClickable(e), 5000);
  }

  waitForNotVisible(selector: string) {
    const e = this.getElement(selector);
    browser.wait(ExpectedConditions.invisibilityOf(e), 5000);
  }

  waitForVisible(selector: string) {
    const e = this.getElement(selector);
    browser.wait(ExpectedConditions.visibilityOf(e), 5000);
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

  getParagraphText() {
    return this.getElement('app-root h1').getText();
  }

  clickElement(selector: string) {
    this.getElement(selector).click();
  }

  clickDropdownItem(label: string, nthItem: number) {
    const dropdownSelector = `[aria-label="${label}"]`;
    const optionSelector = `mat-option:nth-of-type(${nthItem})`;
    this.waitForVisible(dropdownSelector);
    this.clickElement(dropdownSelector);
    this.waitForVisible(optionSelector);
    this.clickElement(optionSelector);
    this.waitForNotVisible(optionSelector);
  }

  isVisible(selector: string) {
    return this.getElement(selector).isDisplayed();
  }

  getElement(selector: string) {
    return element.all(by.css(selector)).first();
  }

  getElements(selector: string) {
    return element.all(by.css(selector));
  }

  getUrl() {
    return browser.getCurrentUrl();
  }

  async getRoute() {
    const url = await this.getUrl();
    return url.split('#')[1];
  }

  inputText(selector: string, textToEnter: string) {
    expect(this.getElements(selector).count()).toEqual(1);
    const field = this.getElement(selector);
    field.sendKeys(textToEnter);
    expect(field.getAttribute('value')).toEqual(textToEnter);
  }

  navigateToHome() {
    return browser.get('/');
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


}
