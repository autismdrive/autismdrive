import {AppPage} from '../app-page.po';

export class AdminUseCases {
  constructor(private page: AppPage) {
  }


  navigateToAdmin() {
    this.page.clickAndExpectRoute('#admin-button', '/admin');
  }

  async navigateToTab(tabNumber: number, selector: string) {
    const tab = this.page.getElement(`.mat-tab-label:nth-child(${tabNumber})`);
    await tab.click();
    await this.page.waitForVisible(selector);
    await expect(tab.getAttribute('aria-selected')).toEqual('true');
  }

  viewAddButton() {
    expect(this.page.getElements('.add-button').count()).toBeGreaterThan(0);
  }

  openForm(buttonSelector, route) {
    this.page.clickAndExpectRoute(buttonSelector, route);
  }
}
