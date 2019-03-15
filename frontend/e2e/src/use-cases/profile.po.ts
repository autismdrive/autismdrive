import { AppPage } from '../app-page.po';

export class ProfileUseCases {
  constructor(private page: AppPage) {
  }

  displayProfileScreen() {
    expect(this.page.getElements('app-profile').count()).toEqual(1);
    expect(this.page.getElements('#enroll_self').count()).toEqual(1);
    expect(this.page.getElements('#enroll_guardian').count()).toEqual(1);
    expect(this.page.getElements('#enroll_professional').count()).toEqual(1);
  }

  startGuardianFlow() {
    const pattern = /\/flow\/guardian_intake\/([0-9]+)/;
    this.page.clickAndExpectRoute('#enroll_guardian', pattern);
  }

  navigateToProfile() {
    this.page.clickAndExpectRoute('#profile-button', '/profile');
  }

  async navigateToGuardianFlow() {
    const btnEl = this.page.getElement('[id^=edit_enroll_self_guardian_');
    const btnId: string = await btnEl.getAttribute('id');
    const participantId = btnId.replace('edit_enroll_self_guardian_', '');
    this.page.clickAndExpectRoute(`#${btnId}`, `/flow/guardian_intake/${participantId}`);
  }
}
