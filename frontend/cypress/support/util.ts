/// <reference types="cypress" />
export class AppPage {
  waitForAngularEnabled() {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    return cy.waitForNetworkIdle(30000);
  }

  navigateToHome() {
    this.navigateTo()
  }

  waitForAnimations() {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    return cy.wait(3000);
  }

  waitForNotVisible(selector: string) {
    return cy.get(selector, {timeout: 30000}).should('not.be.visible');
  }

  waitForVisible(selector: string) {
    return cy.get(selector, {timeout: 30000}).should('be.visible');
  }

  navigateTo(route: string = '/') {
    // cy.viewport('macbook-16');
    return cy.visit(route);
  }

  navigateToUserAdminScreen() {
    this.clickElement('#user-admin-button');
    cy.url().should('match', /#\/admin\/users$/);
    return cy.get('[id^="user_row_"]').should('have.length.gt', 0);
  }

  navigateToUserEditingScreen(selector = '.user-name') {
    return this.getElement(selector).then(el => {
      cy.log(el.attr('id'));
      const idArr = el.attr('id').toString().split('_');
      const userId = idArr[idArr.length - 1];
      cy.get(`#user_row_${userId}`).click();
      cy.url().should('match', new RegExp(`#\/admin\/users\/${userId}$`));
    });
  }

  clickElement(selector: string) {
    return this.getElement(selector).click();
  }

  clickDropdownItem(label: string, nthItem: number, withValue?: string) {
    const dropdownSelector = `[ng-reflect-placeholder="${label}"]`;

    const optionSelector =
      withValue === undefined ? `mat-option:nth-of-type(${nthItem})` : `mat-option[ng-reflect-value="${withValue}"]`;

    this.waitForVisible(dropdownSelector);
    this.clickElement(dropdownSelector);
    cy.get(optionSelector).scrollIntoView().click();
    return this.waitForNotVisible(optionSelector);
  }

  getElement(selector: string) {
    return cy.get(selector).first();
  }

  getElements(selector: string) {
    return cy.get(selector);
  }

  getRandomString() {
    return (Math.random() + 16).toString(36).substring(2);
  }
}
