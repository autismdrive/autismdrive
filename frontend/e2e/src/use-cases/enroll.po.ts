import { AppPage } from '../app-page.po';

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
    const incompleteLinks = await this.page.getElements('app-questionnaire-steps-list .step-link mat-icon.incomplete');
    const completeLinks = await this.page.getElements('app-questionnaire-steps-list .step-link mat-icon.complete');
    expect(completeLinks.length).toEqual(numCompletedSteps);

    const totalNumLinks = incompleteLinks.length + completeLinks.length;
    expect(totalNumLinks).toEqual(numSteps);
  }

  navigateToEachStep() {
    this.page.getElements('app-questionnaire-steps-list .step-link').each(link => {
      link.click();
      this.page.waitForVisible('form');
      this.page.waitForVisible('form h1');
      // this.page.waitForAnimations();
      expect(this.page.getElement('form h1').getText().then(s => s.toLowerCase())).toEqual(link.getText().then(s => s.toLowerCase()));
      expect(this.page.getElements('form mat-form-field').count()).toBeGreaterThan(0);
    });
  }

  cancelEditing() {
    expect(this.page.getElements('#cancel-button').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel-button', '/profile');
  }

  displayTerms() {
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    expect(this.page.getElements('#agree-button').count()).toEqual(1);
    expect(this.page.getElements('#cancel-button').count()).toEqual(1);
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
