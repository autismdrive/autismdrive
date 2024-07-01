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

  completeProfileMetaFormAsGuardian() {
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

  checkDependentButtonDisabled() {
    this.page.getElements('#enroll_first_dependent').should('have.length', 0);
  }

  navigateToProfile() {
    this.page.clickAndExpectRoute('#profile-button', '/profile');
  }

  navigateToProfileMeta() {
    this.page.clickAndExpectRoute('#profile-button', '/profile');
    cy.url().then(function (url) {
      cy.visit(url + '?meta=true');
      cy.get('#meta-form').should('have.length', 1);
    });
  }

  joinRegistry() {
    this.page.clickAndExpectRoute('#join', '/terms/self_guardian');
  }

  displayAvatars() {
    this.page.getElements('[id^=self_participant_').should('have.length.gt', 0);
    this.page.getElements('[id^=self_participant_').each(function ($btnEl) {
      cy.wrap($btnEl)
        .invoke('attr', 'id')
        .then(function (btnId) {
          const participantId = btnId.replace('self_participant_', '');
          cy.get(`#self_participant_${participantId}`).should('have.length', 1);
        });
    });
  }

  displayAvatarDialog() {
    this.page.getElement('[id^=avatar_').click();
    this.page.getElements('app-avatar-dialog').should('have.length', 1);
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

  saveAvatar() {
    cy.get('.avatar').first().as('avatarEl');
    cy.get('@avatarEl').get('img').first().as('avImgEl');
    cy.get('@avImgEl').invoke('css', 'background-color').as('expectedColor');
    cy.get('@avImgEl').invoke('attr', 'src').as('expectedImg');

    cy.get('#save_avatar_changes').click();

    cy.get('app-avatar-dialog').should('have.length', 0);
    cy.get('[id^=avatar_')
      .first()
      .then(function ($avatarBtnEl) {
        const actualColor = $avatarBtnEl.css('background-color');
        const actualImg = $avatarBtnEl.find('img').attr('src');
        cy.wrap($avatarBtnEl).should('have.css', 'background-color', this.expectedColor);
        cy.wrap($avatarBtnEl).get('img').should('have.attr', 'src', this.expectedImg);
        expect(actualImg).to.equal(this.expectedImg);
      });
  }

  navigateToGuardianFlow() {
    const _page = this.page;
    cy.get('[id^=edit_enroll_self_guardian_]')
      .should('be.visible', {timeout: 5000})
      .invoke('attr', 'id')
      .then(function (btnId) {
        const participantId = btnId.replace('edit_enroll_self_guardian_', '');
        _page.clickAndExpectRoute(`#${btnId}`, `/flow/guardian_intake/${participantId}`);
      });
  }

  navigateToDependentFlow() {
    const _page = this.page;
    cy.get('[id^=edit_enroll_dependent_]')
      .should('be.visible', {timeout: 5000})
      .invoke('attr', 'id')
      .then(function (btnId) {
        const participantId = btnId.replace('edit_enroll_dependent_', '');
        _page.clickAndExpectRoute(`#${btnId}`, `/flow/dependent_intake/${participantId}`);
      });
  }
}
