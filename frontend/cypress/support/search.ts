/// <reference types="cypress" />
import {AppPage} from './util';

interface SearchFieldSelectors {
  searchField: string;
  result: string;
  numResultsAttribute: string;
  numResults: string;
  autocomplete: string;
  suggestion: string;
  typeTab: string;
  activeFirstTab: string;
}

export class SearchUseCases {
  constructor(private page: AppPage) {}

  get searchFieldSelectors(): SearchFieldSelectors {
    const autocomplete = '.mat-autocomplete-panel';
    const typeTab = '.type-tabs-container .type-tabs .mat-tab-label';
    const numResultsAttribute = 'data-num-results';
    return {
      searchField: '#search-field input',
      result: 'app-search-result',
      numResultsAttribute,
      numResults: `[${numResultsAttribute}]`,
      autocomplete,
      suggestion: autocomplete + ' .mat-option',
      typeTab,
      activeFirstTab: typeTab + '.mat-tab-label-active[tabindex="0"]',
    };
  }

  checkTypeTabsAndResults(selectors: SearchFieldSelectors) {
    // Wait for type tabs and results to load.
    this.page.waitForVisible(selectors.typeTab);
    this.page.waitForVisible(selectors.result);

    // Verify that type tabs and search results are displayed.
    this.page.getElements(selectors.typeTab).should('have.length', 4).as('numTypeTabsBefore');
    this.page.getElements(selectors.activeFirstTab).should('have.length', 1).as('numFirstTabSelectedAfter');
    return this.page
      .getElement(selectors.numResults)
      .should('be.visible')
      .should('have.attr', selectors.numResultsAttribute)
      .as('numResultsBefore');
  }

  enterKeyword(keywordString: string, selectors: SearchFieldSelectors) {
    // Click the search field.
    this.page.clickElement(selectors.searchField);
    this.page.isVisible(selectors.autocomplete);
    this.page.getElements(selectors.suggestion).should('have.length.gt', 0).should('be.visible');

    // Input keyword
    this.page.inputText(selectors.searchField, keywordString, true);
  }

  checkForResults(selectors: SearchFieldSelectors) {
    this.page.waitForVisible(selectors.result);
    this.page
      .getElement(selectors.numResults)
      .should('be.visible')
      .should('have.attr', selectors.numResultsAttribute)
      .as('numResultsAfter')
      .then(function (numResultsAfter) {
        expect(this.numResultsAfter).to.be.gt(0, 'Keyword search should return results.');
        expect(this.numResultsAfter).to.be.lt(this.numResultsBefore, 'Keyword search should filter the results.');
      });

    // First type tab should be selected.
    this.page.getElements(selectors.typeTab).should('have.length', 4).as('numTypeTabsAfter');
    this.page.getElements(selectors.activeFirstTab).should('have.length', 1).as('numFirstTabSelectedAfter');
    cy.get('@numTypeTabsBefore').then(function (numTypeTabsBefore) {
      expect(this.numTypeTabsAfter).to.equal(this.numTypeTabsBefore, 'All type tabs should be present.');
      expect(this.numFirstTabSelectedAfter).to.equal(
        this.numFirstTabSelectedBefore,
        'First type tab should be selected.',
      );
    });
  }

  enterAutocompleteSearch(keywordString = 'autism') {
    const selectors = this.searchFieldSelectors;

    this.checkTypeTabsAndResults(selectors);
    this.enterKeyword(keywordString, selectors);

    // Select the first autocomplete suggestion
    this.page.isVisible(selectors.autocomplete);
    this.page.isVisible(selectors.suggestion);
    this.page.getElements(selectors.suggestion).should('have.length.gt', 0);
    this.page.clickElement(selectors.suggestion);

    // Verify that the search results are displayed.
    this.checkForResults(selectors);
  }

  enterKeywordsInSearchField(keywordString = 'autism') {
    const selectors = this.searchFieldSelectors;

    this.checkTypeTabsAndResults(selectors).as('numResultsBefore');
    this.enterKeyword(keywordString, selectors);

    // Submit the search
    this.page.pressKey('ENTER');

    // Verify that the search results are displayed.
    this.checkForResults(selectors);

    // Results should be sorted by Relevance
    const selectedSortSelector = '.sort-order app-search-sort mat-select-trigger .selected-sort-label';
    this.page.waitForVisible(selectedSortSelector);
    this.page.getElement(selectedSortSelector).should('have.text', 'Relevance');
  }

  async displaySelectedCategory(filterBy: string) {
    const appliedFilterSelector = '.applied-filters .applied-filter';
    const filterMenuSelector = `.filter-by-${filterBy} .mat-menu-trigger`;
    const filterMenuOptionSelector = '.mat-menu-panel .mat-menu-item:nth-child(2)';
    const appliedFilterChipSelector = `${appliedFilterSelector}-${filterBy}`;
    const numAppliedFiltersBefore = this.page.getElements(appliedFilterSelector).count();
    const numFilterMenus = this.page.getElements(filterMenuSelector).count();
    expect(numFilterMenus).toEqual(1, `Filter menu for ${filterBy} should be visible.`);

    // Open dropdown menu & select first option
    this.page.clickElement(filterMenuSelector);
    this.page.waitForVisible(filterMenuOptionSelector);
    this.page.clickElement(filterMenuOptionSelector);
    this.page.waitForNotVisible(filterMenuOptionSelector);
    this.page.waitForVisible(appliedFilterChipSelector);
    const numAppliedFiltersAfter = this.page.getElements(appliedFilterSelector).count();
    expect(numAppliedFiltersAfter).toBeGreaterThan(numAppliedFiltersBefore);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

  async clearSearchBox(keywordString = 'autism') {
    const searchFieldSelector = '#search-field input';
    const input_text_before = this.page.getElement(searchFieldSelector).getAttribute('value');
    expect(input_text_before.toLowerCase()).toContain(keywordString);

    this.page.clickAndExpectRoute('#logo', '/home');
    this.page.waitForVisible('app-news-item');
    this.page.clickLinkTo('/search');
    this.page.waitForVisible('app-search-result');

    const input_text_after = this.page.getElement(searchFieldSelector).getAttribute('value');
    expect(input_text_after).toEqual('');
  }

  async sortBy(sortMethod: string) {
    const menuSelector = '#sort-and-status .sort-order mat-select';
    const optionSelector = `.mat-option.sort-by-${sortMethod}`;
    this.page.clickElement(menuSelector);
    this.page.waitForVisible(optionSelector);
    this.page.clickElement(optionSelector);
    this.page.waitForNotVisible(optionSelector);
    this.page.waitForAnimations();
  }

  async sortByDistance() {
    this.sortBy('distance');
    expect(this.page.getElements('map-view').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
  }

  // Checks the distance calculation for the each result against the next result.
  // Each result should be closer than the next.
  async checkResultsDistance() {
    const results = this.page.getElements('app-search-result');
    let numChecked = 0;

    for (let i = 0; i < results.length - 1; i++) {
      const thisResult = results[i];
      const nextResult = results[i + 1];
      const thisDistance: string = this.page.getChildElement('app-details-link span.muted', thisResult).getText();
      const nextDistance: string = this.page.getChildElement('app-details-link span.muted', nextResult).getText();

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
    this.openZipCodeDialog();
    this.page.clickElement('#btn_gps');
    const newText = this.page.getElement('#set-location mat-expansion-panel-header').getText();
    expect(newText.includes(zipCode)).toBeFalsy();
  }

  displayResourceAndClickChip() {
    this.page.clickLinkTo('/search');
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
    this.page.waitForVisible(searchResultSelector);
    this.page.waitForVisible(sortOrderSelector + 0 + ' ' + selector);
    this.page.waitForVisible(selectorWithDate);
    const numResults = this.page.getElements(searchResultSelector).count();
    const numWithDate = this.page.getElements(selectorWithDate).count();
    expect(numResults).toBeGreaterThanOrEqual(numWithDate);
    let numChecked = 0;

    for (let i = 0; i < numWithDate - 1; i++) {
      const thisResult = this.page.getElement(sortOrderSelector + i + ' ' + selector);
      const nextResult = this.page.getElement(sortOrderSelector + (i + 1) + ' ' + selector);
      expect(thisResult).toBeTruthy();
      expect(nextResult).toBeTruthy();
      const thisDateStr: string = thisResult.getWebElement().getAttribute(dateAttribute);
      const nextDateStr: string = nextResult.getWebElement().getAttribute(dateAttribute);
      const thisDateInt = new Date(thisDateStr).getTime();
      const nextDateInt = new Date(nextDateStr).getTime();

      if (direction === 'asc') {
        expect(thisDateInt).toBeLessThanOrEqual(nextDateInt);
      } else {
        expect(thisDateInt).toBeGreaterThanOrEqual(nextDateInt);
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
      const numAllResults = this.page.getElements(iconSelector).count();
      const numTypeResults = this.page.getElements(iconTypeSelector).count();
      expect(numAllResults).toEqual(numTypeResults, `All result icons should match type '${keepType}'`);
    }
  }

  async removeFilter(removeChip: string, preserveChip: string) {
    const chipSelector = '.applied-filter';
    const removeChipSelector = `${chipSelector}${chipSelector}-${removeChip}`;
    const preserveChipSelector = `${chipSelector}${chipSelector}-${preserveChip}`;

    const numFiltersBefore = this.page.getElements(chipSelector).count();
    const numRemoveChipsBefore = this.page.getElements(removeChipSelector).count();
    const numPreserveChipsBefore = this.page.getElements(preserveChipSelector).count();
    expect(numRemoveChipsBefore).toEqual(1);

    this.page.clickElement(removeChipSelector);
    this.page.waitFor(500);
    const numFiltersAfter = this.page.getElements(chipSelector).count();
    const numRemoveChipsAfter = this.page.getElements(removeChipSelector).count();
    const numPreserveChipsAfter = this.page.getElements(preserveChipSelector).count();

    expect(numRemoveChipsAfter).toEqual(0);
    expect(numFiltersAfter).toEqual(numFiltersBefore - 1);
    expect(numPreserveChipsAfter).toEqual(numPreserveChipsBefore);
    return expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(0);
  }

  focusAndBlurSearchBox() {
    const searchSelector = '#search-field input';
    this.page.isFocused(searchSelector);
    this.page.pressKey('ESCAPE');
  }

  async goToNextResultsPage() {
    const selector = '.mat-paginator-range-label';
    const headingSelector = '.search-result-status h4';
    expect(this.page.getElement(selector).getText()).toMatch(/^1 – 20 of/);
    expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 1-20 of/);
    this.page.clickElement('button[aria-label="Next page"]');
    this.page.waitForVisible('app-search-result');
    expect(this.page.getElement(selector).getText()).toMatch(/^21 – 40 of/);
    expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 21-40 of/);
  }

  async goBackAndCheckPageNum() {
    const resultSelector = 'app-search-result a.title';
    const selector = '.mat-paginator-range-label';
    const headingSelector = '.search-result-status h4';
    const titleBefore = this.page.getElement('h1').getText();
    this.page.goBack();
    this.page.waitForVisible(resultSelector);
    const titleAfter = this.page.getElement(resultSelector).getText();
    expect(titleBefore).toEqual(titleAfter);
    expect(this.page.getElement(selector).getText()).toMatch(/^21 – 40 of/);
    expect(this.page.getElement(headingSelector).getText()).toMatch(/^Showing 21-40 of/);
  }
}
