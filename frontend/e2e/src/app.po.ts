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

  navigateToHome() {
    return browser.get('/');
  }

  async clickLinkTo(route: string) {
    this.waitForClickable(`[ng-reflect-router-link=${route}]`);
    this.clickElement(`[ng-reflect-router-link=${route}]`);
    const url = await this.getUrl();
    expect(url.split('#')[1]).toEqual(route);
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
}
