/// <reference types="cypress" />
import Chainable = Cypress.Chainable;

export type ElementResults = Cypress.Chainable<JQuery<HTMLElement>>;

export class AppPage {
  constructor() {
    this.maximize();
  }

  maximize() {
    return cy.viewport('macbook-13');
  }

  resizeTo(width: number, height: number) {
    return cy.viewport(width, height);
  }

  waitFor(t: number) {
    return cy.wait(t);
  }

  waitForText(selector: string, text: string) {
    return cy.get(selector).should('have.text', text, {timeout: 5000});
  }

  waitForAnimations() {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    return cy.wait(3000);
  }

  waitForStale(selector: string) {
    return cy.get(selector).should('not.exist', {timeout: 5000});
  }

  waitForClickable(selector: string) {
    cy.get(selector).should('be.enabled', {timeout: 5000}).should('be.visible', {timeout: 5000});
  }

  waitForNotVisible(selector: string) {
    return cy.get(selector).should('not.be.visible', {timeout: 5000});
  }

  // If given CSS selector is found on the page, waits 5 seconds for the element to become visible. If it's not found
  // on the page, recursively calls itself maxLoops number of times, waiting 1 second between each call, until the
  // element becomes present.
  waitForVisible(selector: string) {
    return cy.get(selector).should('be.visible', {timeout: 5000});
  }

  getLocalStorageVar(name: string): Cypress.Chainable<string> {
    return cy.window().its('localStorage').invoke('getItem', name);
  }

  getSessionStorageVar(key: string) {
    return cy.window().its('sessionStorage').invoke('getItem', key);
  }

  clickLinkTo(route: string) {
    const selector = `[href="#${route}"]`;
    this.waitForClickable(selector);
    this.clickElement(selector);
    this.getRoute().should('eq', route);
  }

  clickLinkToVariation(route: string) {
    const selector = `[href="#${route}"]`;
    this.waitForClickable(selector);
    this.clickElement(selector);
    this.getRoute().should('equal', route);
  }

  getParagraphText() {
    return this.getElement('app-root h1').invoke('text');
  }

  clickElement(selector: string) {
    this.waitForClickable(selector);
    this.scrollTo(selector);
    this.focus(selector);
    this.isFocused(selector);
    return cy.get(selector).click();
  }

  clickDropdownItem(dropdownSelector: string, nthItem: number) {
    const optionSelector = `mat-option:nth-of-type(${nthItem})`;
    this.waitForVisible(dropdownSelector);
    this.clickElement(dropdownSelector);
    this.waitForVisible(optionSelector);
    this.clickElement(optionSelector);
    this.waitForNotVisible(optionSelector);
  }

  isVisible(selector: string) {
    return this.getElement(selector).should('be.visible');
  }

  getElement(selector: string): ElementResults {
    return cy.get(selector).first();
  }

  getElements(selector: string): ElementResults {
    return cy.get(selector);
  }

  getChildElement(selector: string, parentElement: ElementResults): ElementResults {
    return this.getChildElements(selector, parentElement).first();
  }

  getChildElements(selector: string, parentElement: ElementResults) {
    return parentElement.get(selector);
  }

  getUrl() {
    return cy.location('href');
  }

  getRoute() {
    return cy.location('hash');
  }

  pressKey(keyCode: string) {
    return cy.focused().type(keyCode);
  }

  focus(selector: string) {
    cy.get(selector).focus();
  }

  isFocused(selector: string) {
    return cy.get(selector).should('be.focused');
  }

  inputText(selector: string, textToEnter: string, clearFirst?: boolean) {
    this.waitForClickable(selector);
    this.clickElement(selector);

    if (clearFirst) {
      cy.get(selector).clear();
      cy.get(selector).should('have.value', '');
    }

    cy.get(selector).type(textToEnter);
    cy.get(selector).should('have.value', textToEnter);

    this.getElements(selector).should('have.length', 1);
    this.waitForVisible(selector);
  }

  navigateToUrl(url: string) {
    return cy.visit(url);
  }

  navigateToHome() {
    return cy.request('/');
  }

  refresh() {
    return cy.reload();
  }

  clickAndExpectRoute(clickSelector: string, expectedRoute: string | RegExp) {
    this.clickElement(clickSelector);
    if (typeof expectedRoute === 'string') {
      this.getRoute().should('equal', expectedRoute);
    } else {
      this.getRoute().should('match', expectedRoute);
    }
  }

  getRandomString(length: number) {
    const s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    return Array(length)
      .join()
      .split(',')
      .map(() => s.charAt(Math.floor(Math.random() * s.length)))
      .join('');
  }

  getRandomNumString(length: number) {
    const s = '123456789';
    return Array(length)
      .join()
      .split(',')
      .map(() => s.charAt(Math.floor(Math.random() * s.length)))
      .join('');
  }

  getRandomDate(start: Date, end: Date): Date {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
  }

  scrollTo(selector: string) {
    return cy.get(selector).scrollIntoView();
  }

  tabThroughAllFields() {
    this.focus('formly-form');

    const selector =
      '' +
      'formly-field [id*="_input_"],' +
      'formly-field [id*="_datepicker_"],' +
      'formly-field [id*="_radio_"],' +
      'formly-field [id*="_checkbox_"],' +
      'formly-field [id*="_select_"]';

    this.getElements(selector).each(_ => this.pressKey('TAB'));
  }

  fillOutFields(selector: string) {
    const _page = this;
    this.getElements(selector).each(function ($el) {
      const _e = cy.wrap($el);
      _e.should('have.attr', 'id').as('fieldId');
      _page.scrollTo(`#${this.fieldId}`);


      const id = _e.getAttribute('id');
      if (id) {
        this.scrollTo(`#${id}`);

        if (/_input_email_/.test(id)) {
          const email = this.getRandomString(8) + '@whatever.com';
          _e.sendKeys(email);
        } else if (/_input_phone_/.test(id)) {
          const phone = this.getRandomNumString(10);
          _e.sendKeys(phone);
        } else if (/_input_zip_/.test(id)) {
          const zip = this.getRandomNumString(5);
          _e.sendKeys(zip);
        } else if (/_input_/.test(id)) {
          _e.getAttribute('type').then(eType => {
            let str = '';

            if (eType === 'number') {
              str = this.getRandomNumString(2);
            } else {
              str = this.getRandomString(16);
            }
            _e.sendKeys(str);
          });
        } else if (/_datepicker_/.test(id)) {
          const date = this.getRandomDate(new Date(2000, 0, 1), new Date());
          const mm = date.getMonth() + 1;
          const dd = date.getDate();
          const yyyy = date.getFullYear();
          const dateStr = `${mm}/${dd}/${yyyy}`;
          _e.clear();
          _e.sendKeys(dateStr);
        } else if (/_radio_/.test(id)) {
          _e.$(`#${id}_0 .mat-radio-container`).click();
        } else if (/_checkbox_/.test(id)) {
          _e.$(`#${id}_0`).click();
        } else if (/_select_/.test(id)) {
          _e.click();
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


    })





  }

  goBack() {
    return browser.executeScript('window.history.back()');
  }
}
