import { AppPage } from '../app-page.po';
import {by} from 'protractor';

export class EnrollUseCases {
  constructor(private page: AppPage) {
  }

  async displayMenuLinks() {
    const numStepsStr: string = await this.page.getElement('#num_total_steps').getText();
    const numSteps = parseInt(numStepsStr, 10);
    const menuLinks = await this.page.getElements('app-questionnaire-steps-list .step-link');
    expect(menuLinks.length).toEqual(numSteps);
  }

  async displayCompletedStatus() {
    const numStepsStr: string = await this.page.getElement('#num_total_steps').getText();
    const numSteps = parseInt(numStepsStr, 10);
    const numCompletedStepsStr: string = await this.page.getElement('#num_completed_steps').getText();
    const numCompletedSteps = parseInt(numCompletedStepsStr, 10);
    const incompleteLinks = await this.page.getElements('app-questionnaire-steps-list .step-link .done mat-icon.hidden');
    const completeLinks = await this.page.getElements('app-questionnaire-steps-list .step-link .done mat-icon.visible');
    expect(completeLinks.length).toEqual(numCompletedSteps);
    const totalNumLinks = incompleteLinks.length + completeLinks.length;
    expect(totalNumLinks).toEqual(numSteps);
  }

  navigateToEachStep() {
    this.page.getElements('app-questionnaire-steps-list .step-link').each(link => {
      const link_span = link.element(by.css('.step-link-text')).getWebElement();
      link.click();
      this.page.waitForVisible('form');
      this.page.waitForVisible('form h1');
      // this.page.waitForAnimations();
      expect(this.page.getElement('form h1').getText().then(s => s.toLowerCase())).toEqual(link_span.getText().then(s => s.toLowerCase()));
      expect(this.page.getElements('form mat-form-field').count()).toBeGreaterThan(0);
    });
  }

  cancelIntro() {
    this.page.waitFor(3000);
    expect(this.page.getElements('#intro-cancel-button').count()).toEqual(1);
    this.page.clickAndExpectRoute('#intro-cancel-button', '/profile');
  }

  cancelEditing() {
    expect(this.page.getElements('#flow-cancel-button').count()).toEqual(1);
    this.page.clickAndExpectRoute('#flow-cancel-button', '/profile');
  }

  displayGuardianTerms() {
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    expect(this.page.getElements('#guardian-terms').count()).toEqual(1);
    expect(this.page.getElements('#agree-button').count()).toEqual(1);
    expect(this.page.getElements('#terms-cancel-button').count()).toEqual(1);
  }

  cancelTerms() {
    expect(this.page.getElements('#terms-cancel-button').count()).toEqual(1);
    this.page.clickAndExpectRoute('#terms-cancel-button', '/profile');
  }

  acceptTerms() {
    expect(this.page.getElements('#agree-button').count()).toEqual(1);
    this.page.clickElement('#agree-button');
    expect(this.page.getElements('app-flow-intro').count()).toEqual(1);
  }

  displayInstructions() {
    expect(this.page.getElements('app-flow-intro').count()).toEqual(1);
    expect(this.page.getElements('#instructions').count()).toEqual(1);
    expect(this.page.getElements('#next-button').count()).toEqual(1);
    expect(this.page.getElements('[id*="_input_"]').count()).toEqual(0);
    this.page.clickElement('#next-button');
    expect(this.page.getElements('[id*="_input_"]').count()).toBeGreaterThanOrEqual(1);
  }

  fillOutRequiredFields() {
    expect(this.page.getElements('#save-next-button[disabled]').count()).toEqual(1);
    expect(this.page.getElements('.mat-form-field-required-marker').count()).toBeGreaterThanOrEqual(1);
    this.page.tabThroughAllFields();
    expect(this.page.getElements('.ng-invalid').count()).toBeGreaterThan(0);
    this.page.fillOutInvalidFields();
    expect(this.page.getElements('#save-next-button[disabled]').count()).toEqual(0);
    expect(this.page.getElements('mat-error formly-validation-message').count()).toEqual(0);
  }
}
