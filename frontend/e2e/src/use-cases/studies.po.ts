import {AppPage} from '../app-page.po';

export class StudiesUseCases {
  constructor(private page: AppPage) {
  }

  navigateToStudiesPage() {
    this.page.clickLinkTo('/studies/currently_enrolling');
    expect(this.page.getElements('.studies').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
  }

  async filterByStatus(selectStatus?: string) {
    const tiles = await this.page.getElements('#hero app-border-box-tile');
    expect(tiles.length).toEqual(4);

    for (const tile of tiles) {
      const selectedStatus = await tile.getAttribute('data-study-status');
      expect(selectedStatus).toBeTruthy();

      // If no specific status was given, click each tile in sequence
      // Otherwise, only click the one we care about.
      if (!selectStatus || (selectStatus && (selectStatus === selectedStatus))) {
        tile.click();
        await this.checkResultsMatchStatus(selectedStatus);
      }
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
      return expect(this.page.getElement('p[data-study-status]').getAttribute('data-study-status')).toEqual(selectedStatus);
    }
  }
}
