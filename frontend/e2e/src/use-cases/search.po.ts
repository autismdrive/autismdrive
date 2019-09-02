import { AppPage } from '../app-page.po';
import { ElementFinder } from 'protractor';

export class SearchUseCases {
  constructor(private page: AppPage) {
  }

  enterKeywordsInSearchField() {
    expect(this.page.getElements('app-search-result').count()).toEqual(0);
    this.page.clickLinkTo('/home');
    this.page.inputText('#site-header .search-bar input', 'autism');
    this.page.pressKey('ENTER');
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

  async displaySelectedFilters() {
    expect(this.page.getElements('.filters').count()).toEqual(1);
    expect(this.page.getElements('.filters-topics .filter-facet-item').count()).toBeGreaterThan(1);

    const num_filters_before = await this.page.getElements('.applied-filters .applied-filter').count();
    expect(num_filters_before).toEqual(1);

    const filter = await this.page.getElements('.filters-topics .filter-facet-item').first();
    filter.click();

    const num_filters_after = await this.page.getElements('.applied-filters .applied-filter').count();
    expect(num_filters_after).toEqual(2);

    const filter_text = await filter.$('.filter-facet-label').getText();
    const applied_filter_text = await this.page.getElements('.applied-filters .applied-filter .applied-filter-label').last().getText();
    expect(filter_text).toEqual(applied_filter_text);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }
}
