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

    const firstResult = this.page.getElements('app-search-result').first();
    const lastResult = this.page.getElements('app-search-result').last();
    const firstDistance: string = await this.page.getChildElement('app-details-link span.muted', firstResult).getText();
    const lastDistance: string = await this.page.getChildElement('app-details-link span.muted', lastResult).getText();

    // Extract number of miles from details link text: (1.23MI) --> 1.23
    const pattern = /\(([\d]+)\.([\d]+)MI\)/;
    const firstNum = parseFloat(firstDistance.replace(pattern, '$1.$2'));
    const lastNum = parseFloat(lastDistance.replace(pattern, '$1.$2'));
    expect(firstNum).toBeLessThan(lastNum);
  }

  async setZipCode() {
    const zipCode = '24401'
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"] button');
    this.page.waitForAnimations();

    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.inputText('mat-dialog-container [placeholder="ZIP Code"]', zipCode);
    this.page.clickElement('#btn_save');
    this.page.waitForAnimations();

    const newText: string = await this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]').getText();
    expect(newText.includes(zipCode)).toBeTruthy();
  }

  async clearZipCode() {
    const zipCode = '24401'
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"] button');
    this.page.waitForAnimations();

    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.clickElement('#btn_gps');
    this.page.waitForAnimations();

    const newText: string = await this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]').getText();
    expect(newText.includes(zipCode)).toBeFalsy();
  }
}
