/// <reference types="cypress" />
import {AppPage} from './util';

export class AdminUseCases {
  constructor(private page: AppPage) {}

  navigateToAdmin() {
    this.page.clickAndExpectRoute('#admin-button', '/admin/data-admin');
  }

  async navigateToTab(tabId: string, selector: string) {
    const tab = this.page.getElement(tabId);
    await tab.click();
    await this.page.waitForVisible(selector);
    await expect(tab.getAttribute('ng-reflect-active')).toEqual('true');
  }

  viewAddButton() {
    expect(this.page.getElements('.add-button').count()).toBeGreaterThan(0);
  }

  openForm(buttonSelector, route) {
    this.page.clickAndExpectRoute(buttonSelector, route);
  }
}
