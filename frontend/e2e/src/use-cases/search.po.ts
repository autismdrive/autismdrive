import { AppPage } from '../app-page.po';

export class SearchUseCases {
  constructor(private page: AppPage) {
  }

  enterKeywordsInSearchField() {
    expect(this.page.getElements('app-search-result').count()).toEqual(0);
    this.page.clickLinkTo('/home');
    this.page.inputText('#site-header .search-bar input', 'autism');
    this.page.pressKey('ENTER');
    this.page.waitForVisible('app-search-result');
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

  async clearSearchBox() {
    const input_text_before = await this.page.getElement('#site-header .search-bar input').getAttribute('value');
    expect(input_text_before).toEqual('autism');

    this.page.clickLinkTo('/home');

    const input_text_after = await this.page.getElement('#site-header .search-bar input').getAttribute('value');
    expect(input_text_after).toEqual('');
  }

  async sortByDistance() {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]');
    this.page.waitForAnimations();
    expect(this.page.getElements('agm-map').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
  }

  // Checks the distance calculation for the first result against the last result.
  // The last result should be farther away than the last result.
  async checkResultsDistance() {
    const results = await this.page.getElements('app-search-result');
    let numChecked = 0;

    for (let i = 0; i < results.length - 1; i++) {
      const thisResult = results[i];
      const nextResult = results[i + 1];
      const thisDistance: string = await this.page.getChildElement('app-details-link span.muted', thisResult).getText();
      const nextDistance: string = await this.page.getChildElement('app-details-link span.muted', nextResult).getText();

      // Extract number of miles from details link text: (1.23MI) --> 1.23
      const pattern = /\(([\d]+)\.([\d]+)MI\)/;
      const thisNum = parseFloat(thisDistance.replace(pattern, '$1.$2'));
      const nextNum = parseFloat(nextDistance.replace(pattern, '$1.$2'));
      expect(thisNum).toBeLessThanOrEqual(nextNum);
      numChecked++;
    }

    expect(numChecked).toEqual(results.length - 1);
  }

  openZipCodeDialog() {
    const distSelector = '.sort-order mat-radio-group [ng-reflect-value="Distance"]';
    this.page.clickElement(`${distSelector} button`);
    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.waitForVisible('mat-dialog-container');
    this.page.waitFor(1000);
  }

  enterZipCode(zipCode = '24401') {
    this.page.inputText('mat-dialog-container [placeholder="ZIP Code"]', zipCode, true);
    this.page.clickElement('#btn_save');
    this.page.waitForNotVisible('mat-dialog-container');
    this.page.waitFor(1000);
  }

  checkSavedZipCode(zipCode = '24401') {
    const distSelector = '.sort-order mat-radio-group [ng-reflect-value="Distance"]';
    this.page.waitForText(distSelector, zipCode);
    this.page.waitFor(1000);
    expect(this.page.getLocalStorageVar('zipCode')).toEqual(zipCode);
    expect(this.page.getElement(distSelector).getText()).toContain(zipCode);
  }

  async clearZipCode(zipCode = '24401') {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"] button');
    this.page.waitFor(1000);

    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.clickElement('#btn_gps');
    this.page.waitFor(1000);

    const newText = await this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]').getText()
    expect(newText.includes(zipCode)).toBeFalsy();
  }
}
