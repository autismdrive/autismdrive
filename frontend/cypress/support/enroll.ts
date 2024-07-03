/// <reference types="cypress" />
import {AppPage} from './util';

export class EnrollUseCases {
  constructor(private page: AppPage) {}

  displayMenuLinks() {
    this.page.getElement('#num_total_steps').invoke('text').as('numSteps');
    this.page.getElements('app-questionnaire-steps-list .step-link').then(function ($links) {
      expect($links.length).to.equal(parseInt(this.numSteps));
    });
  }

  displayCompletedStatus() {
    this.page.getElement('#num_total_steps').invoke('text').as('numSteps');
    this.page.getElement('#num_completed_steps').invoke('text').as('numCompletedSteps');
    this.page.getElements('app-questionnaire-steps-list .step-link .done mat-icon.hidden').as('incompleteLinks');
    this.page.getElements('app-questionnaire-steps-list .step-link .done mat-icon.visible').as('completeLinks');
    cy.get('@completeLinks').then(function ($completeLinks) {
      expect($completeLinks.length).to.equal(parseInt(this.numCompletedSteps));

      cy.get('@incompleteLinks').then(function ($incompleteLinks) {
        expect($incompleteLinks.length + $completeLinks.length).to.equal(parseInt(this.numSteps));
      });
    });
  }

  navigateToEachStep() {
    const _page = this.page;
    _page.getElements('app-questionnaire-steps-list .step-link').each(function ($el) {
      cy.wrap($el).get('.step-link-text').click();
      _page.waitForVisible('form');
      _page
        .waitForVisible('form h1')
        .invoke('text')
        .then(function (s) {
          cy.wrap($el).should('have.text', s, {matchCase: false});
        });
      _page.getElements('form mat-form-field').should('have.length.gt', 0);
    });
  }

  cancelIntro() {
    this.page.waitFor(3000);
    this.page.getElements('#intro-cancel-button').should('have.length', 1);
    this.page.clickAndExpectRoute('#intro-cancel-button', '#/profile');
  }

  cancelEditing() {
    this.page.waitForVisible('#flow-cancel-button');
    this.page.getElements('#flow-cancel-button').should('have.length', 1);
    this.page.clickAndExpectRoute('#flow-cancel-button', '#/profile');
  }

  displayGuardianTerms() {
    this.page.getElements('app-terms').should('have.length', 1);
    this.page.getElements('#guardian-terms').should('have.length', 1);
    this.page.getElements('#agree-button').should('have.length', 1);
    this.page.getElements('#terms-cancel-button').should('have.length', 1);
  }

  cancelTerms() {
    this.page.getElements('#terms-cancel-button').should('have.length', 1);
    this.page.clickAndExpectRoute('#terms-cancel-button', '#/profile');
  }

  acceptTerms() {
    this.page.getElements('#agree-button').should('have.length', 1);
    this.page.clickElement('#agree-button');
    this.page.getElements('app-flow-intro').should('have.length', 1);
  }

  displayInstructions() {
    this.page.waitForVisible('app-flow-intro');
    this.page.getElements('app-flow-intro').should('have.length', 1);
    this.page.getElements('#instructions').should('have.length', 1);
    this.page.getElements('#next-button').should('have.length', 1);
    this.page.getElements('[id*="_input_"]').should('have.length', 0);
    this.page.clickElement('#next-button');
    this.page.getElements('[id*="_input_"]').should('have.length.gte', 1);
  }

  fillOutRequiredFields(
    self,
    reqSelector: string,
    btnSelector: string,
    invalidSelector: string,
    highlightSelector: string,
  ) {
    this._fillOutRequiredFieldsRecursive(self, reqSelector, btnSelector, invalidSelector, highlightSelector);
    this.page.getElements(btnSelector).should('have.length', 0);
  }

  _fillOutRequiredFieldsRecursive(
    self,
    reqSelector: string,
    btnSelector: string,
    invalidSelector: string,
    highlightSelector: string,
  ) {
    const _self = self;
    const _page = _self.page;
    _page.clickElement(highlightSelector);
    _page.waitFor(300);
    _page
      .getElements(invalidSelector)
      .invoke('length')
      .then(function (numInvalidBefore) {
        if (numInvalidBefore > 0) {
          _page.getElements(btnSelector).should('have.length', 1);
          _page.fillOutFields(invalidSelector);
          return _self._fillOutRequiredFieldsRecursive(
            _self,
            reqSelector,
            btnSelector,
            invalidSelector,
            highlightSelector,
          );
        } else {
          _page.getElements(invalidSelector).should('have.length', 0);
          _page.getElements(btnSelector).should('have.length', 0);
        }
      });
  }

  saveStep(stepIndex: number) {
    const selector = `#step_link_${stepIndex}`;
    const _page = this.page;
    _page.getElement(selector).invoke('attr', 'id').as('currentStepId');
    _page.clickElement('#save-next-button');
    _page.waitFor(500);
    _page.waitForVisible('#save-next-button, app-flow-complete').then(function (_) {
      _page.getElements(`#${this.currentStepId} .done .visible`).should('have.length', 1);
    });
  }

  completeStep(stepIndex: number) {
    const selector = `#step_link_${stepIndex}`;
    this.page.getElement(selector).click();
    this.page.getElements(`${selector} .done .visible`).should('have.length', 0);

    this.fillOutRequiredFields(
      this,
      '.mat-form-field-required-marker',
      '#save-next-button.disabled',
      '.ng-invalid',
      '#highlight-required-fields',
    );
    this.fillOutRepeatSections();
    this.page.waitFor(1000);
    this.saveStep(stepIndex);
    this.page.waitFor(1000);
    this.page.getElements(`${selector} .done .visible`).should('have.length', 1);
  }

  fillOutRepeatSections() {
    const _self = this;
    const _page = this.page;
    const itemSelector = 'mat-card.repeat';
    const dialogSelector = 'app-repeat-section-dialog .mat-dialog-content';
    const saveBtnSelector = 'app-repeat-section-dialog .repeat-section-dialog-save';
    cy.get('app-repeat-section').as('repeatSections');
    cy.get('@repeatSections').then(function ($repeatSections) {
      const numRepeats = $repeatSections.length;
      cy.get(itemSelector).should('have.length', numRepeats);
    });

    cy.get('@repeatSections').each(function ($repeatSection) {
      _page.getElements(dialogSelector).should('not.be.visible');
      cy.wrap($repeatSection).get(itemSelector).should('have.length', 0);
      cy.wrap($repeatSection).get('.repeat-action button').click();
      _page.waitForVisible(dialogSelector);
      _page.waitFor(100);

      _self.fillOutRequiredFields(
        _self,
        `${dialogSelector} .mat-form-field-required-marker`,
        `${saveBtnSelector}.disabled`,
        `${dialogSelector} .ng-invalid`,
        '#highlight-required-fields-in-dialog',
      );
      _page.waitFor(100);
      _page.waitForNotVisible(`${saveBtnSelector}.disabled`);
      _page.waitForClickable(saveBtnSelector);
      _page.waitFor(100);

      // Click dialog
      _page.getElements(dialogSelector).each(function ($el) {
        _page.waitFor(100);
        cy.wrap($el).click();
        _page.waitFor(100);
      });

      _page.waitForNotVisible(dialogSelector);
      cy.wrap($repeatSection).get(itemSelector).should('have.length', 1);
      _page.getElements(dialogSelector).should('have.length', 0);
      _page.waitFor(100);
    });
  }
}
