import {AppPage} from '../app-page.po';

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

  async displaySelectedCategory(filterClass: string) {
    const filterSelector = '.applied-filters .applied-filter';
    const filterClassSelector = `.filter-by-${filterClass}`;

    expect(this.page.getElements('.filters-column').count()).toEqual(1);
    expect(this.page.getElements(filterClassSelector).count()).toEqual(1);
    expect(await this.page.getElements(filterSelector).count()).toEqual(1);

    this.page.clickElement(filterClassSelector);

    expect(this.page.getElements(filterSelector).count()).toEqual(2);

    const category_text = await this.page.getElement(`${filterClassSelector} .filter-facet-label`).getText();
    const applied_filter_text = await this.page.getElement(`${filterSelector}-${filterClass}`).getText();
    expect(applied_filter_text).toContain(category_text);
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

  // Checks the distance calculation for the each result against the next result.
  // Each result should be closer than the next.
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

  async openZipCodeDialog() {
    const numDialogs = await this.page.getElements('mat-dialog-container').count();

    if (numDialogs === 0) {
      const distSelector = '.sort-order mat-radio-group [ng-reflect-value="Distance"]';
      this.page.clickElement(`${distSelector} button`);
      expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
      this.page.waitForVisible('mat-dialog-container');
      this.page.waitFor(500);
    }
  }

  enterZipCode(zipCode = '24401') {
    this.page.inputText('mat-dialog-container [placeholder="ZIP Code"]', zipCode, true);
    this.page.clickElement('#btn_save');
    this.page.waitForNotVisible('mat-dialog-container');
    this.page.waitFor(500);
  }

  checkSavedZipCode(zipCode = '24401') {
    const distSelector = '.sort-order mat-radio-group [ng-reflect-value="Distance"]';
    this.page.waitForText(distSelector, zipCode);
    this.page.waitFor(500);
    expect(this.page.getLocalStorageVar('zipCode')).toEqual(zipCode);
    expect(this.page.getElement(distSelector).getText()).toContain(zipCode);
  }

  async clearZipCode(zipCode = '24401') {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Distance"] button');
    this.page.waitFor(500);

    expect(this.page.getElements('mat-dialog-container').count()).toEqual(1);
    this.page.clickElement('#btn_gps');
    this.page.waitFor(500);

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
    expect(this.page.getElements('.applied-filter').count()).toEqual(1);
  }

  sortByEventDate() {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Event Date"]');
    this.page.waitFor(1000);
    return this.checkResultsDates('.hit-event-date', 'asc');
  }

  sortByLastUpdated() {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Updated"]');
    this.page.waitFor(1000);
    return this.checkResultsDates('.hit-last-updated', 'desc');
  }

  // Checks each date in the search results with the date of the result after it.
  // Each date should be less than the next one.
  async checkResultsDates(selector: string, direction: string) {
    await this.page.waitForVisible(selector);
    const results = await this.page.getElements(selector);
    const isoSelector = 'data-iso-date-string';
    let numChecked = 0;
    const numTotal = results.length - 1;

    await expect(results.length).toBeGreaterThan(0);
    for (let i = 0; i < results.length - 1; i++) {
      const thisResult = results[i];
      const nextResult = results[i + 1];
      const thisDateStr: string = await thisResult.getAttribute(isoSelector);
      const nextDateStr: string = await nextResult.getAttribute(isoSelector);
      const thisDateInt = new Date(thisDateStr).getTime();
      const nextDateInt = new Date(nextDateStr).getTime();

      if (direction === 'asc') {
        await expect(thisDateInt).toBeLessThanOrEqual(nextDateInt);
      } else {
        await expect(thisDateInt).toBeGreaterThanOrEqual(nextDateInt);
      }
      numChecked++;
    }

    return expect(numChecked).toEqual(numTotal);
  }

  async removeFilter(removeChip: string, preserveChip: string) {
    const chipSelector = '.applied-filter';
    const removeChipSelector = `${chipSelector}${chipSelector}-${removeChip}`;
    const preserveChipSelector = `${chipSelector}${chipSelector}-${preserveChip}`;

    const numFiltersBefore = await this.page.getElements(chipSelector).count();
    const numRemoveChipsBefore = await this.page.getElements(removeChipSelector).count();
    const numPreserveChipsBefore = await this.page.getElements(preserveChipSelector).count();
    await expect(numRemoveChipsBefore).toEqual(1);

    await this.page.clickElement(removeChipSelector);
    await this.page.waitFor(500);
    const numFiltersAfter = await this.page.getElements(chipSelector).count();
    const numRemoveChipsAfter = await this.page.getElements(removeChipSelector).count();
    const numPreserveChipsAfter = await this.page.getElements(preserveChipSelector).count();

    await expect(numRemoveChipsAfter).toEqual(0);
    await expect(numFiltersAfter).toEqual(numFiltersBefore - 1);
    await expect(numPreserveChipsAfter).toEqual(numPreserveChipsBefore);
    return expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }
}
