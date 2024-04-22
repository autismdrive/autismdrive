import {AppPage} from '../app-page.po';

export class SearchUseCases {
  constructor(private page: AppPage) {}

  async enterKeywordsInSearchField(keywordString = 'autism', autocomplete = true) {
    const searchFieldSelector = '#search-field input';
    const resultSelector = 'app-search-result';
    const numResultsAttribute = 'data-num-results';
    const numResultsSelector = '[data-num-results]';
    const autocompleteSelector = '.mat-autocomplete-panel';
    const suggestionSelector = autocompleteSelector + ' .mat-option';
    const typeTabSelector = '.type-tabs-container .type-tabs .mat-tab-label';
    const activeFirstTabSelector = typeTabSelector + '.mat-tab-label-active[tabindex="0"]';

    // Wait for type tabs and results to load.
    await this.page.waitForVisible(typeTabSelector);
    await this.page.waitForVisible(resultSelector);

    // Verify that type tabs and search results are displayed.
    const numResultsBefore = parseInt(
      await this.page.getElement(numResultsSelector).getWebElement().getAttribute(numResultsAttribute),
      10,
    );
    expect(numResultsBefore).toBeGreaterThan(0, 'Search results should be visible.');
    const numTypeTabsBefore = await this.page.getElements(typeTabSelector).count();
    expect(numTypeTabsBefore).toEqual(4, 'All type tabs should be present.');
    const numFirstTabSelectedBefore = await this.page.getElements(activeFirstTabSelector).count();
    expect(numFirstTabSelectedBefore).toEqual(1, 'First type tab should be selected.');

    // Click the search field.
    this.page.clickElement(searchFieldSelector);
    const autocompleteIsVisibleBefore = await this.page.isVisible(autocompleteSelector);
    expect(autocompleteIsVisibleBefore).toEqual(true, 'Autocomplete panel should be visible.');
    const numSuggestionsBefore = await this.page.getElements(suggestionSelector).count();
    expect(numSuggestionsBefore).toBeGreaterThan(0, 'Search suggestions should be visible.');

    // Input keyword
    this.page.inputText(searchFieldSelector, keywordString);

    if (autocomplete) {
      const autocompleteIsVisibleAfter = await this.page.isVisible(autocompleteSelector);
      expect(autocompleteIsVisibleAfter).toEqual(true);
      const suggestionIsVisibleAfter = await this.page.isVisible(suggestionSelector);
      expect(suggestionIsVisibleAfter).toEqual(true);
      const numSuggestionsAfter = await this.page.getElements(suggestionSelector).count();
      expect(numSuggestionsAfter).toBeGreaterThan(0, 'Search suggestions should be visible.');

      // Select the first suggestion
      this.page.clickElement(suggestionSelector);
    } else {
      // Submit the search
      this.page.pressKey('ENTER');
    }

    this.page.waitForVisible(resultSelector);
    const numResultsAfter = parseInt(
      await this.page.getElement(numResultsSelector).getWebElement().getAttribute(numResultsAttribute),
      10,
    );
    expect(numResultsAfter).toBeGreaterThan(0, 'Keyword search should return results.');
    expect(numResultsAfter).toBeLessThan(numResultsBefore, 'Keyword search should filter the results.');

    // First type tab should be selected.
    const numTypeTabsAfter = await this.page.getElements(typeTabSelector).count();
    const numFirstTabSelectedAfter = await this.page.getElements(activeFirstTabSelector).count();
    expect(numTypeTabsAfter).toEqual(numTypeTabsBefore, 'All type tabs should be present.');
    expect(numFirstTabSelectedAfter).toEqual(numFirstTabSelectedBefore, 'First type tab should be selected.');

    if (!autocomplete) {
      // Results should be sorted by Relevance
      const selectedSortSelector = '.sort-order app-search-sort mat-select-trigger .selected-sort-label';
      await this.page.waitForVisible(selectedSortSelector);
      const selectEl = await this.page.getElement(selectedSortSelector);
      expect(selectEl.getText()).toEqual('Relevance');
    }
  }

  async displaySelectedCategory(filterBy: string) {
    const appliedFilterSelector = '.applied-filters .applied-filter';
    const filterMenuSelector = `.filter-by-${filterBy} .mat-menu-trigger`;
    const filterMenuOptionSelector = '.mat-menu-panel .mat-menu-item:nth-child(2)';
    const appliedFilterChipSelector = `${appliedFilterSelector}-${filterBy}`;
    const numAppliedFiltersBefore = await this.page.getElements(appliedFilterSelector).count();
    const numFilterMenus = await this.page.getElements(filterMenuSelector).count();
    expect(numFilterMenus).toEqual(1, `Filter menu for ${filterBy} should be visible.`);

    // Open dropdown menu & select first option
    this.page.clickElement(filterMenuSelector);
    await this.page.waitForVisible(filterMenuOptionSelector);
    this.page.clickElement(filterMenuOptionSelector);
    await this.page.waitForNotVisible(filterMenuOptionSelector);
    await this.page.waitForVisible(appliedFilterChipSelector);
    const numAppliedFiltersAfter = await this.page.getElements(appliedFilterSelector).count();
    expect(numAppliedFiltersAfter).toBeGreaterThan(numAppliedFiltersBefore);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

  async clearSearchBox(keywordString = 'autism') {
    const searchFieldSelector = '#search-field input';
    const input_text_before = await this.page.getElement(searchFieldSelector).getAttribute('value');
    expect(input_text_before.toLowerCase()).toContain(keywordString);

    this.page.clickAndExpectRoute('#logo', '/home');
    this.page.waitForVisible('app-news-item');
    this.page.clickLinkToVariation('/search');
    this.page.waitForVisible('app-search-result');

    const input_text_after = await this.page.getElement(searchFieldSelector).getAttribute('value');
    expect(input_text_after).toEqual('');
  }

  async sortBy(sortMethod: string) {
    const menuSelector = '#sort-and-status .sort-order mat-select';
    const optionSelector = `.mat-option.sort-by-${sortMethod}`;
    this.page.clickElement(menuSelector);
    await this.page.waitForVisible(optionSelector);
    this.page.clickElement(optionSelector);
    await this.page.waitForNotVisible(optionSelector);
    await this.page.waitForAnimations();
  }

  async sortByDistance() {
    this.sortBy('distance');
    expect(this.page.getElements('map-view').count()).toEqual(1);
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
    this.page.inputText('mat-form-field [placeholder="Enter ZIP Code"]', zipCode, true);
    this.page.clickElement('#btn_save');
  }

  checkSavedZipCode(zipCode = '24401') {
    const distSelector = '#set-location mat-expansion-panel-header';
    this.page.waitForText(distSelector, zipCode);
    this.page.waitFor(500);
    expect(this.page.getLocalStorageVar('zipCode')).toEqual(zipCode);
    expect(this.page.getElement(distSelector).getText()).toContain(zipCode);
  }

  async clearZipCode(zipCode = '24401') {
    await this.openZipCodeDialog();
    this.page.clickElement('#btn_gps');
    const newText = await this.page.getElement('#set-location mat-expansion-panel-header').getText();
    expect(newText.includes(zipCode)).toBeFalsy();
  }

  displayResourceAndClickChip() {
    this.page.clickLinkToVariation('/search');
    this.displayResource();
    this.page.clickElement('mat-chip');
    this.page.waitForVisible('.applied-filter');
    expect(this.page.getElements('.applied-filter').count()).toEqual(1);
  }

  displayResource() {
    this.page.waitForVisible('app-search-result');
    this.page.getElements('.result-item div a').first().click();
    this.page.waitForVisible('app-resource-detail');
  }

  sortByEventDate() {
    this.sortBy('date');
    return this.checkResultsDates('.hit-event-date', 'asc');
  }

  sortByLastUpdated() {
    this.sortBy('updated');
    return this.checkResultsDates('.hit-last-updated', 'desc');
  }

  // Checks each date in the search results with the date of the result after it.
  // Each date should be less than the next one.
  async checkResultsDates(selector: string, direction: string) {
    const dateAttribute = 'data-iso-date-string';
    const searchResultSelector = `app-search-result[class*='sort-order-']`;
    const sortOrderSelector = '.sort-order-';
    const selectorWithDate = selector + `[${dateAttribute}]`;
    await this.page.waitForVisible(searchResultSelector);
    await this.page.waitForVisible(sortOrderSelector + 0 + ' ' + selector);
    await this.page.waitForVisible(selectorWithDate);
    const numResults = await this.page.getElements(searchResultSelector).count();
    const numWithDate = await this.page.getElements(selectorWithDate).count();
    expect(numResults).toBeGreaterThanOrEqual(numWithDate);
    let numChecked = 0;

    for (let i = 0; i < numWithDate - 1; i++) {
      const thisResult = await this.page.getElement(sortOrderSelector + i + ' ' + selector);
      const nextResult = await this.page.getElement(sortOrderSelector + (i + 1) + ' ' + selector);
      expect(thisResult).toBeTruthy();
      expect(nextResult).toBeTruthy();
      const thisDateStr: string = await thisResult.getWebElement().getAttribute(dateAttribute);
      const nextDateStr: string = await nextResult.getWebElement().getAttribute(dateAttribute);
      const thisDateInt = new Date(thisDateStr).getTime();
      const nextDateInt = new Date(nextDateStr).getTime();

      if (direction === 'asc') {
        await expect(thisDateInt).toBeLessThanOrEqual(nextDateInt);
      } else {
        await expect(thisDateInt).toBeGreaterThanOrEqual(nextDateInt);
      }
      numChecked++;
    }

    return expect(numChecked).toEqual(numWithDate - 1);
  }

  async filterByType(keepType: string) {
    const showAll = keepType === 'all';
    const tabSelector = `.type-buttons.${keepType}`;
    const selectedTabSelector = `.mat-tab-label-active ${tabSelector}`;
    const iconSelector = `app-search-result app-type-icon`;
    const iconTypeSelector = iconSelector + `[ng-reflect-icon-type='${showAll ? 'location' : keepType}']`;
    const appliedFilterSelector = '.applied-filter.applied-filter-type';
    this.page.clickElement(tabSelector);
    expect(this.page.isVisible(selectedTabSelector)).toEqual(true);
    this.page.waitForVisible(iconTypeSelector);

    if (showAll) {
      expect(this.page.getElements(appliedFilterSelector).count()).toEqual(
        0,
        'Should not filter by type when All Resources tab is clicked.',
      );
    } else {
      expect(this.page.getElements(appliedFilterSelector).count()).toEqual(1, `Should filter by '${keepType}'`);
      const numAllResults = await this.page.getElements(iconSelector).count();
      const numTypeResults = await this.page.getElements(iconTypeSelector).count();
      expect(numAllResults).toEqual(numTypeResults, `All result icons should match type '${keepType}'`);
    }
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

  focusAndBlurSearchBox() {
    const searchSelector = '#search-field input';
    expect(this.page.isFocused(searchSelector)).toBeTruthy();
    this.page.pressKey('ESCAPE');
  }

  async goToNextResultsPage() {
    const selector = '.mat-paginator-range-label';
    const headingSelector = '.search-result-status h4';
    await expect(this.page.getElement(selector).getText()).toMatch(/^1 – 20 of/);
    await expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 1-20 of/);
    await this.page.clickElement('button[aria-label="Next page"]');
    await this.page.waitForVisible('app-search-result');
    await expect(this.page.getElement(selector).getText()).toMatch(/^21 – 40 of/);
    await expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 21-40 of/);
  }

  async goBackAndCheckPageNum() {
    const resultSelector = 'app-search-result a.title';
    const selector = '.mat-paginator-range-label';
    const headingSelector = '.search-result-status h4';
    const titleBefore = await this.page.getElement('h1').getText();
    await this.page.goBack();
    await this.page.waitForVisible(resultSelector);
    const titleAfter = await this.page.getElement(resultSelector).getText();
    expect(titleBefore).toEqual(titleAfter);
    await expect(this.page.getElement(selector).getText()).toMatch(/^21 – 40 of/);
    await expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 21-40 of/);
  }
}
