/// <reference types="cypress" />
import {AppPage} from './util';

export class AdminUseCases {
  constructor(private page: AppPage) {}

  navigateToAdmin() {
    this.page.clickAndExpectRoute('#admin-button', '/admin/data-admin');
  }

  async navigateToTab(tabId: string, selector: string) {
    this.page.clickElement(tabId);
    this.page.waitForVisible(selector);
    this.page.getElement(tabId).should('have.attr', 'ng-reflect-active', 'true');
  }

  viewAddButton() {
    this.page.getElements('.add-button').should('have.length.gt', 0);
  }

  openForm(buttonSelector, route) {
    this.page.clickAndExpectRoute(buttonSelector, route);
  }
}
