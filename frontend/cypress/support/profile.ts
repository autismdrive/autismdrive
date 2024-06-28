/// <reference types="cypress" />
import {AppPage} from './util';

export class ProfileUseCases {
  constructor(private page: AppPage) {}

  clickFormlyBox() {
    cy.get('input')
      .as('inputs')
      .filter((index, input) => document.evaluate('model[options.key]', input).stringValue === 'modelName')
      .first()
      .type('some text');
  }

  async completeProfileMetaFormAsGuardian() {
    cy.get('#meta-form').should('have.length', 1);

    // Get  'formly-field [id*="_checkbox_"],' +
    cy.get('formly-field.guardian label').click();
    cy.get('formly-field.guardian input').should('be.selected');

    cy.get('formly-field.guardian_has_dependent label').click();
    cy.get('formly-field.guardian input').should('be.selected');

    cy.get('#submit_meta').click();
    cy.get('#self_guardian').should('have.length', 1);

    cy.get('formly-field.guardian_has_dependent').get('mat-radio-button').click({multiple: true});
    cy.get('#submit_meta').click();
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

  editAvatarImg() {
    return cy
      .get('.avatar-image')
      .as('btnEl')
      .each(($el, index) => {
        if (index < 2) {
          cy.wrap($el).click();
          cy.get('.avatar img')
            .invoke('attr', 'src')
            .then(avImgSrc => {
              cy.get('@btnEl').get('img').should('have.attr', 'src', avImgSrc);
            });
        }
      });
  }

  editAvatarColor() {
    return cy.get('.color-swatch').each(($el, index) => {
      cy.wrap($el).click();
      cy.get('.avatar').should('have.css', 'background-color', $el.css('background-color'));
    });
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
