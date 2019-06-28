import { AppPage } from '../app-page.po';
import { ElementFinder } from 'protractor';

export class SearchUseCases {
  constructor(private page: AppPage) {
  }

  enterKeywordsInSearchField() {
    expect(this.page.getElements('app-search-result').count()).toEqual(0);
    this.page.clickLinkTo('/home');
    this.page.inputText('#site-header .search-bar input', 'autism');
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

  async displaySelectedFilters() {
    expect(this.page.getElements('.sidenav.filters').count()).toEqual(1);
    expect(this.page.getElements('.sidenav.filters .filter-facet').count()).toBeGreaterThan(1);
    expect(this.page.getElements('.applied-filters .applied-filter').count()).toEqual(1);

    const facet = await this.page.getElements('.sidenav.filters .filter-facet').first();
    facet.$('mat-panel-title').click();
    this.page.waitForAnimations();
    facet.$$('.filter-facet-item').first().click();
    expect(this.page.getElements('.applied-filters .applied-filter').count()).toBeGreaterThan(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

}
