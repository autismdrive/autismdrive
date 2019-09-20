import { AppPage } from '../app-page.po';
import {browser, ExpectedConditions} from 'protractor';

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
    const relevance_radio = this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Relevance"]');
    expect(relevance_radio.isSelected());
  }

  removeSearchTerm() {
    const applied_filter = this.page.getElement('.applied-filters .applied-filter-keyword');
    expect(browser.getCurrentUrl()).toContain('words=autism');
    applied_filter.click();
    expect(browser.getCurrentUrl()).not.toContain('words=autism');
  }

  async filterByAge() {

    this.page.clickElement('#filter_pre-k');
    const applied_filter = await this.page.getElement('#remove_filter_pre-k');
    browser.wait(ExpectedConditions.urlContains('ages='), 5000);

    // Remove the age filter, and wait for it to go away.
    applied_filter.click();

    // Assure that it is removed from the display, and in the browser url (so history is updated)
    expect(applied_filter.isPresent()).toEqual(false);
    expect(browser.getCurrentUrl()).not.toContain('ages=');
  }

  async goHomeClearsSearch() {
    this.page.inputText('#site-header .search-bar input', 'autism', true);
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
//    this.page.waitForVisible('mat-dialog-container');
//    this.page.waitFor(1000);
  }

  enterZipCode(zipCode = '24401') {
    this.page.inputText('mat-dialog-container [placeholder="ZIP Code"]', zipCode, true);
    this.page.clickElement('#btn_save');
  }

  async checkSavedZipCode(zipCode = '24401') {
    const distSelector = '.sort-order mat-radio-group [ng-reflect-value="Distance"]';
    this.page.waitForText(distSelector, zipCode);
    expect(this.page.getLocalStorageVar('zipCode')).toEqual(zipCode);
    expect(this.page.getElement(distSelector).getText()).toContain(zipCode);
  }

  async clearZipCode(zipCode = '24401') {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"] button');

    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.clickElement('#btn_gps');

    const newText = await this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]').getText();
    expect(newText.includes(zipCode)).toBeFalsy();
  }

  displayResourceAndClickChip() {
    this.page.clickLinkTo('/search');
    this.page.waitForVisible('app-search-result');
    this.page.getElements('.result-item div a').first().click();
    this.page.waitForVisible('app-resource-detail');

    this.page.clickElement('mat-chip');
    this.page.waitForVisible('.applied-filter');
    return expect(this.page.getElements('.applied-filter').count()).toEqual(1);
  }
}
