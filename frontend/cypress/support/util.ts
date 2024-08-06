/// <reference types="cypress" />
import Chainable = Cypress.Chainable;
import {faker} from '@node_modules/@faker-js/faker';

export type ElementResults = Cypress.Chainable<JQuery<HTMLElement>>;

export class AppPage {
  constructor() {
    this.maximize();
  }

  maximize() {
    return cy.viewport('macbook-15');
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
    cy.get(selector).should('be.visible', {timeout: 5000}).and('not.be.disabled');
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

  waitForNetworkIdle(waitMs: number = 5000) {
    return cy.waitForNetworkIdle(waitMs);
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

  getText(selector: string) {
    return this.getElement(selector).invoke('text');
  }

  getParagraphText() {
    return this.getElement('app-root h1').invoke('text');
  }

  clickElement(selector: string) {
    this.waitForClickable(selector);
    this.scrollTo(selector);
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
    cy.get(selector).trigger('mouseover');
    cy.get(selector).trigger('focusin');
  }

  isFocused(selector: string) {
    return cy.get(selector).should('be.focused');
  }

  getInputStringForFieldId(id: string, fieldType: string): string {
    const d = faker.date.past();
    const dStr = `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`;

    const patternMap = [
      {pattern: '_input_email_', type: 'text', str: faker.internet.email()},
      {pattern: '_input_phone_', type: 'text', str: faker.phone.number()},
      {pattern: '_input_zip_', type: 'text', str: faker.location.zipCode()},
      {pattern: '_input_', type: 'number', str: faker.number.int().toString()},
      {pattern: '_input_', type: 'text', str: faker.internet.password({length: 16})},
      {pattern: '_datepicker_', type: 'text', str: dStr},
      {pattern: '_radio_', type: 'text', str: ' '},
      {pattern: '_checkbox_', type: 'text', str: ' '},
      {pattern: '_select_', type: 'text', str: ' '},
    ];

    for (const {pattern, type, str} of patternMap) {
      if (id.includes(pattern) && fieldType === type) {
        return str;
      }
    }
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
    cy.visit(url);
    this.waitForNetworkIdle();
  }

  navigateToHome() {
    this.navigateToUrl('/');
  }

  refresh() {
    cy.reload();
    this.waitForNetworkIdle();
  }

  clickAndExpectRoute(clickSelector: string, expectedRoute: string | RegExp) {
    this.clickElement(clickSelector);
    if (typeof expectedRoute === 'string') {
      this.getRoute().should('equal', expectedRoute);
    } else {
      this.getRoute().should('match', expectedRoute);
    }
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
      cy.wrap($el).as('fieldEl');
      cy.get('@fieldEl').should('have.attr', 'id').as('fieldId');
      cy.get('@fieldEl').should('have.attr', 'type').as('fieldType');
      const fieldSelector = `#${this.fieldId}`;
      _page.scrollTo(fieldSelector);
      const inputString = _page.getInputStringForFieldId(this.fieldId, this.fieldType);
      _page.inputText(fieldSelector, inputString, true);

      if (/_select_/.test(this.fieldId)) {
        cy.get('@fieldEl').click();

        const optionSelector = 'mat-option:first-of-type';
        _page.waitForVisible(optionSelector);
        _page.getElement(optionSelector).click();
        _page.waitForNotVisible(optionSelector);

        const multicheckboxSelector = `${selector} formly-field-mat-multicheckbox mat-checkbox:first-of-type`;
        _page.getElements(multicheckboxSelector).should('have.length.greaterThan', 0);
        _page.getElements(`${multicheckboxSelector} .mat-checkbox-inner-container`).click({multiple: true});
      }
    });
  }

  goBack() {
    cy.go('back');
  }
}
