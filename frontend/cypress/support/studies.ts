/// <reference types="cypress" />
import {AppPage} from './util';

export class StudiesUseCases {
  constructor(private page: AppPage) {}

  navigateToStudiesPage() {
    this.page.clickLinkTo('/studies');
    this.page.getElements('.studies').should('have.length', 1);
    this.page.getElements('app-search-result').should('have.length.gt', 1);
  }

  filterBy(selectStatus?: string) {
    const menuSelector = '#set-status';
    const optionSelector = `.mat-option.sort-by-${selectStatus}`;
    this.page.clickElement(menuSelector);
    this.page.waitForVisible(optionSelector);
    this.page.clickElement(optionSelector);
    this.page.waitForNotVisible(optionSelector);
    this.page.waitForAnimations();
  }
  filterByStatus(selectStatus?: string) {
    this.filterBy(selectStatus);

    this.page.getElement('[data-study-status]').then($el => {
      const selectedStatus = $el.attr('data-study-status');
      expect(selectedStatus).not.to.be.empty;

      if (!selectStatus || (selectStatus && selectStatus === selectedStatus)) {
        this.filterBy(selectStatus);
        this.checkResultsMatchStatus(selectStatus);
      }
    });
  }

  checkResultsMatchStatus(selectedStatus: string) {
    this.page.getElements('app-search-result').then($els => {
      if ($els.length > 0) {
        // Check that status of all displayed results matches selected status
        this.page.getElements('app-search-result').each(result => {
          cy.wrap(result).should('have.attr', 'data-study-status', selectedStatus);

          if (selectedStatus === 'currently_enrolling') {
            this.page.getElements('.status-badge.status-currently-enrolling').should('have.length.gt', 0);
          }
        });
      } else {
        // Check that the "no results" message matches the selected status
        this.page.getElement('p[data-study-status]').should('have.attr', 'data-study-status', selectedStatus);
      }
    });
  }
}
