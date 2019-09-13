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
    this.page.waitForVisible('#flow-cancel-button');
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
    this.page.waitForVisible('app-flow-intro');
    expect(this.page.getElements('app-flow-intro').count()).toEqual(1);
    expect(this.page.getElements('#instructions').count()).toEqual(1);
    expect(this.page.getElements('#next-button').count()).toEqual(1);
    expect(this.page.getElements('[id*="_input_"]').count()).toEqual(0);
    this.page.clickElement('#next-button');
    expect(this.page.getElements('[id*="_input_"]').count()).toBeGreaterThanOrEqual(1);
  }

  async fillOutRequiredFields() {
    const btnSelector = '#save-next-button.disabled';
    const reqSelector = '.mat-form-field-required-marker';

    const numRequired = await this.page.getElements(reqSelector).count();
    if (numRequired === 0) {
      await expect(this.page.getElements(btnSelector).count()).toEqual(0);
    } else {
      await expect(this.page.getElements(btnSelector).count()).toEqual(1);
      await this.page.clickElement(btnSelector);
      await expect(this.page.getElements('.ng-invalid').count()).toBeGreaterThan(0);
      await this.page.fillOutInvalidFields();
      await this.page.waitFor(500);
    }

    await expect(this.page.getElements(btnSelector).count()).toEqual(0);
  }

  async saveStep() {
    const selector = '.mat-list-item.step-link.active';
    const currentStepId = await this.page.getElement(selector).getAttribute('id');
    await this.page.clickElement('#save-next-button');
    await this.page.waitFor(500);
    await this.page.waitForVisible('#save-next-button, app-flow-complete');
    await expect(this.page.getElements(`#${currentStepId} .done .visible`).count()).toEqual(1);
  }

  async completeAllSteps() {
    const selector = '.mat-list-item.step-link';
    const numStepsTotal = await this.page.getElements(selector).count();
    const numStepsComplete = await this.page.getElements(`${selector} .done .visible`).count();
    const numStepsToDo = numStepsTotal - numStepsComplete;

    for (let i = 0; i < numStepsToDo; i++) {
      await this.fillOutRequiredFields();
      await this.page.waitFor(500);
      await this.saveStep();
      await this.page.waitFor(500);
    }

    const numDone = await this.page.getElements(`${selector} .done .visible`).count();
    expect(numDone).toEqual(numStepsTotal);
  }
}
