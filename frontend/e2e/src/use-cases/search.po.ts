import {AppPage} from '../app-page.po';

export class SearchUseCases {
  constructor(private page: AppPage) {
  }

  async enterKeywordsInSearchField() {
    const searchFieldSelector = '#search-field input';
    const resultSelector = 'app-search-result';
    const autocompleteSelector = '.mat-autocomplete-panel';
    const suggestionSelector = autocompleteSelector + ' .mat-option';
    const typeTabSelector = '.type-tabs-container .type-tabs .mat-tab-label';
    const activeFirstTabSelector = typeTabSelector + '.mat-tab-label-active#mat-tab-label-0-0';

    const numResultsBefore = await this.page.getElements(resultSelector).count();
    expect(numResultsBefore).toBeGreaterThan(0, 'Search results should be visible.');
    const numTypeTabsBefore = await this.page.getElements(typeTabSelector).count();
    expect(numTypeTabsBefore).toEqual(4, 'All type tabs should be present.');
    const numFirstTabSelectedBefore = await this.page.getElements(activeFirstTabSelector).count();
    expect(numFirstTabSelectedBefore).toEqual(1, 'First type tab should be selected.');

    // Click the search field
    this.page.clickElement(searchFieldSelector);
    const autocompleteIsVisibleBefore = await this.page.isVisible(autocompleteSelector);
    expect(autocompleteIsVisibleBefore).toEqual(false);
    const numSuggestionsBefore = await this.page.getElements(suggestionSelector).count();
    expect(numSuggestionsBefore).toEqual(0, 'No suggestions should be visible yet.');

    // Input keyword
    this.page.inputText(searchFieldSelector, 'ad');
    const autocompleteIsVisibleAfter = await this.page.isVisible(autocompleteSelector);
    expect(autocompleteIsVisibleAfter).toEqual(true);
    const suggestionIsVisibleAfter = await this.page.isVisible(suggestionSelector);
    expect(suggestionIsVisibleAfter).toEqual(true);
    const numSuggestionsAfter = await this.page.getElements(suggestionSelector).count();
    expect(numSuggestionsAfter).toBeGreaterThan(0, 'Search suggestions should be visible.');

    // Select the first suggestion
    this.page.clickElement(suggestionSelector);
    this.page.waitForVisible(resultSelector);
    const numResultsAfter = await this.page.getElements(resultSelector).count();
    expect(numResultsAfter).toBeGreaterThan(0, 'Keyword search should return results.');
    expect(numResultsAfter).toBeLessThan(numResultsBefore, 'Keyword search should filter the results.');

    // First type tab should be selected.
    const numTypeTabsAfter = await this.page.getElements(typeTabSelector).count();
    const numFirstTabSelectedAfter  = await this.page.getElements(activeFirstTabSelector).count();
    expect(numTypeTabsAfter).toEqual(numTypeTabsBefore, 'All type tabs should be present.');
    expect(numFirstTabSelectedAfter).toEqual(numFirstTabSelectedBefore, 'First type tab should be selected.');
  }

  async clearKeywordSearch() {

  }

  async displaySelectedCategory(filterBy: string) {
    const appliedFilterSelector = '.applied-filters .applied-filter';
    const filterMenuSelector = `.filter-by-${filterBy} mat-select`;
    const filterMenuOptionSelector = '.mat-select-panel .mat-option[ng-reflect-value]';
    const appliedFilterChipSelector = `${appliedFilterSelector}-${filterBy}`;

    const numAppliedFiltersBefore = await this.page.getElements(appliedFilterSelector).count();
    expect(numAppliedFiltersBefore).toEqual(0, 'No applied filters should be visible yet.');

    const numFilterMenus = await this.page.getElements(filterMenuSelector).count();
    expect(numFilterMenus).toEqual(1, `Filter menu for ${filterBy} should be visible.`);

    // Open dropdown menu & select first option
    this.page.clickElement(filterMenuSelector);
    await this.page.waitForVisible(filterMenuOptionSelector);
    this.page.clickElement(filterMenuOptionSelector);
    await this.page.waitForNotVisible(filterMenuOptionSelector);
    await this.page.waitForVisible(appliedFilterChipSelector);
    const numAppliedFiltersAfter = await this.page.getElements(appliedFilterSelector).count();
    expect(numAppliedFiltersAfter).toEqual(1);
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
    const menuSelector = '#sort-and-status .sort-order mat-select';
    const optionSelector = '.mat-option.sort-by-distance';
    this.page.clickElement(menuSelector);
    await this.page.waitForVisible(optionSelector);
    this.page.clickElement(optionSelector);
    await this.page.waitForNotVisible(optionSelector);
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
    expect(this.page.isVisible('#set-location')).toEqual(true);
    expect(this.page.isVisible('.zipCodeSetButton')).toEqual(true);
    expect(this.page.isVisible('.zipCodeField')).toEqual(false);

    this.page.clickElement('.zipCodeSetButton');
    expect(this.page.isVisible('.zipCodeField')).toEqual(true);
  }

  enterZipCode(zipCode = '24401') {
    this.page.inputText('mat-form-field [placeholder="ZIP Code"]', zipCode, true);
    this.page.clickElement('#btn_save');
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
    this.page.clickElement('#btn_gps');

    const newText = await this.page.getElement('.sort-order mat-radio-group [ng-reflect-value="Distance"]').getText();
    expect(newText.includes(zipCode)).toBeFalsy();
  }

  displayResourceAndClickChip() {
    this.page.clickLinkToVariation('/search');
    this.page.waitForVisible('app-search-result');
    this.page.getElements('.result-item div a').first().click();
    this.page.waitForVisible('app-resource-detail');

    this.page.clickElement('mat-chip');
    this.page.waitForVisible('.applied-filter');
    expect(this.page.getElements('.applied-filter').count()).toEqual(1);
  }

  sortByEventDate() {
    this.page.clickElement('.sort-order mat-radio-group [ng-reflect-value="Date"]');
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
