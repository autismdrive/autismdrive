import {AppPage} from '../app-page.po';

export class StudiesUseCases {
  constructor(private page: AppPage) {}

  navigateToStudiesPage() {
    this.page.clickLinkToVariation('/studies');
    expect(this.page.getElements('.studies').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
  }

  async filterBy(selectStatus?: string) {
    const menuSelector = '#set-status';
    const optionSelector = `.mat-option.sort-by-${selectStatus}`;
    this.page.clickElement(menuSelector);
    await this.page.waitForVisible(optionSelector);
    this.page.clickElement(optionSelector);
    await this.page.waitForNotVisible(optionSelector);
    await this.page.waitForAnimations();
  }
  async filterByStatus(selectStatus?: string) {
    await this.filterBy(selectStatus);
    const selectedStatus = this.page.getElement('data-study-status');
    expect(selectedStatus).toBeTruthy();
    if (!selectStatus || (selectStatus && selectStatus === (await selectedStatus))) {
      this.filterBy(selectStatus);
      await this.checkResultsMatchStatus(selectStatus);
    }
  }

  async checkResultsMatchStatus(selectedStatus: string) {
    const numResults = await this.page.getElements('app-search-result').count();

    if (numResults > 0) {
      // Check that status of all displayed results matches selected status
      return this.page.getElements('app-search-result').each(result => {
        expect(result.getAttribute('data-study-status')).toEqual(selectedStatus);

        if (selectedStatus === 'currently_enrolling') {
          expect(this.page.getElements('.status-badge.status-currently-enrolling').count()).toBeGreaterThan(0);
        }
      });
    } else {
      // Check that the "no results" message matches the selected status
      return expect(this.page.getElement('p[data-study-status]').getAttribute('data-study-status')).toEqual(
        selectedStatus,
      );
    }
  }
}
