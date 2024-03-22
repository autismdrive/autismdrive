/// <reference types="cypress" />
import {AppPage} from './util';

export class ProfileUseCases {
  constructor(private page: AppPage) {}

  clickFormlyBox() {
    const formlyInputs = cy.get('input');
    const desiredModel = 'modelName';
    const desiredInput = formlyInputs
      .filter(function (input) {
        return input.evaluate('model[options.key]').then(function (model) {
          return model === desiredModel;
        });
      })
      .first();
    desiredInput.sendKeys('some text');
  }

  async completeProfileMetaFormAsGuardian() {
    expect(this.page.getElements('#meta-form').count()).toEqual(1);
    // Get  'formly-field [id*="_checkbox_"],' +
    this.page.getElement('formly-field.guardian label').click();
    expect(this.page.getElement('formly-field.guardian input').isSelected()).toBeTruthy();

    this.page.getElement('formly-field.guardian_has_dependent label').click();
    expect(this.page.getElement('formly-field.guardian input').isSelected()).toBeTruthy();

    this.page.getElement('#submit_meta').click();

    expect(this.page.getElements('#self_guardian').count()).toEqual(1);
    /**
    const radio = this.page.getElement( 'formly-field.guardian_has_dependent').all('mat-radio-button');
    radio.click();


    await this.page.clickElement('#submit_meta');
***/
  }

  startDependentFlow() {
    this.page.clickAndExpectRoute('#enroll_dependent', '/terms/dependent');
  }

  async checkDependentButtonDisabled() {
    const numButtons = await this.page.getElements('#enroll_first_dependent').count();
    return expect(numButtons).toEqual(
      0,
      'No dependent enroll button should be visible if guardian has not completed their profile yet.',
    );
  }

  navigateToProfile() {
    this.page.clickAndExpectRoute('#profile-button', '/profile');
  }

  async navigateToProfileMeta() {
    this.page.clickAndExpectRoute('#profile-button', '/profile');
    let currentLoc = await browser.getCurrentUrl();
    browser.get(currentLoc + '?meta=true');
    await this.page.getElements('#meta-form');
  }

  async joinRegistry() {
    this.page.clickAndExpectRoute('#join', '/terms/self_guardian');
  }

  async displayAvatars() {
    expect(this.page.getElements('[id^=self_participant_').count()).toBeGreaterThan(0);
    const btnEls = await this.page.getElements('[id^=self_participant_');
    for (const btnEl of btnEls) {
      const btnId: string = await btnEl.getAttribute('id');
      const participantId = btnId.replace('self_participant_', '');
      expect(this.page.getElements('#self_participant_' + participantId).count()).toEqual(1);
    }
  }

  async displayAvatarDialog() {
    const btnEl = this.page.getElement('[id^=avatar_');
    const btnId: string = await btnEl.getAttribute('id');
    this.page.clickElement(`#${btnId}`);
    expect(this.page.getElements('app-avatar-dialog').count()).toEqual(1);
  }

  async editAvatarImg() {
    const btnEls = await this.page.getElements('.avatar-image');

    for (let i = 0; i < btnEls.length; i++) {
      const btnEl = btnEls[i];

      if (i < 2) {
        btnEl.click();
        const avImgEl = this.page.getElement('.avatar img');
        const imgEl = this.page.getChildElement('img', btnEl);
        const expectedSrc = await imgEl.getAttribute('src');
        const actualSrc = await avImgEl.getAttribute('src');
        expect(expectedSrc).toEqual(actualSrc);
      }
    }
  }

  async editAvatarColor() {
    const swatchEls = await this.page.getElements('.color-swatch');

    for (let i = 0; i < swatchEls.length; i++) {
      const swatchEl = swatchEls[i];

      if (i < 2) {
        swatchEl.click();
        const avatar = this.page.getElement('.avatar');
        const expectedColor = await swatchEl.getCssValue('background-color');
        const actualColor = await avatar.getCssValue('background-color');
        expect(expectedColor).toEqual(actualColor);
      }
    }
  }

  async saveAvatar() {
    const avatarEl = this.page.getElement('.avatar');
    const avImgEl = this.page.getChildElement('img', avatarEl);
    const expectedColor = await avatarEl.getCssValue('background-color');
    const expectedImg = await avImgEl.getAttribute('src');
    this.page.clickElement('#save_avatar_changes');
    expect(this.page.getElements('app-avatar-dialog').count()).toEqual(0);
    const avatarBtnEl = this.page.getElement('[id^=avatar_');
    const actualColor = await avatarBtnEl.getCssValue('background-color');
    const actualImg = await avatarBtnEl.getAttribute('src');
    expect(expectedColor).toEqual(actualColor);
    expect(expectedImg).toEqual(actualImg);
  }

  async navigateToGuardianFlow() {
    this.page.waitForVisible('[id^=edit_enroll_self_guardian_]');
    const btnEl = this.page.getElement('[id^=edit_enroll_self_guardian_]');
    const btnId: string = await btnEl.getAttribute('id');
    const participantId = btnId.replace('edit_enroll_self_guardian_', '');
    this.page.clickAndExpectRoute(`#${btnId}`, `/flow/guardian_intake/${participantId}`);
  }

  async navigateToDependentFlow() {
    this.page.waitForVisible('[id^=edit_enroll_dependent_]');
    const btnEl = this.page.getElement('[id^=edit_enroll_dependent_]');
    const btnId: string = await btnEl.getAttribute('id');
    const participantId = btnId.replace('edit_enroll_dependent_', '');
    this.page.clickAndExpectRoute(`#${btnId}`, `/flow/dependent_intake/${participantId}`);
  }
}
