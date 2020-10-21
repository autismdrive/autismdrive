  import { AppPage } from '../app-page.po';
import {by, ElementFinder} from 'protractor';

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

  async fillOutRequiredFields(reqSelector: string, btnSelector: string, invalidSelector: string, highlightSelector: string) {
    await this._fillOutRequiredFieldsRecursive(reqSelector, btnSelector, invalidSelector, highlightSelector);
    return expect(this.page.getElements(btnSelector).count()).toEqual(0);
  }

  async _fillOutRequiredFieldsRecursive(reqSelector: string, btnSelector: string, invalidSelector: string, highlightSelector: string) {
    await this.page.clickElement(highlightSelector);
    await this.page.waitFor(300);
    const numInvalidBefore = await this.page.getElements(invalidSelector).count();

    if (numInvalidBefore > 0) {
      await expect(this.page.getElements(btnSelector).count()).toEqual(1);
      await this.page.fillOutFields(invalidSelector);
      return this._fillOutRequiredFieldsRecursive(reqSelector, btnSelector, invalidSelector, highlightSelector);
    } else {
      await expect(this.page.getElements(invalidSelector).count()).toEqual(0);
      await expect(this.page.getElements(btnSelector).count()).toEqual(0);
    }
  }

  async saveStep(stepIndex: number) {
    const selector = `#step_link_${stepIndex}`;
    const currentStepId = await this.page.getElement(selector).getAttribute('id');
    await this.page.clickElement('#save-next-button');
    await this.page.waitFor(500);
    await this.page.waitForVisible('#save-next-button, app-flow-complete');
    return expect(this.page.getElements(`#${currentStepId} .done .visible`).count()).toEqual(1);
  }

  async completeStep(stepIndex: number) {
    const selector = `#step_link_${stepIndex}`;
    this.page.getElement(selector).click();
    expect(this.page.getElements(`${selector} .done .visible`).count()).toEqual(0);

    await this.fillOutRequiredFields(
      '.mat-form-field-required-marker',
      '#save-next-button.disabled',
      '.ng-invalid',
      '#highlight-required-fields'
    );
    await this.fillOutRepeatSections();
    await this.page.waitFor(1000);
    await this.saveStep(stepIndex);
    await this.page.waitFor(1000);
    expect(this.page.getElements(`${selector} .done .visible`).count()).toEqual(1);
  }

  async fillOutRepeatSections() {
    const itemSelector = 'mat-card.repeat';
    const dialogSelector = 'app-repeat-section-dialog .mat-dialog-content';
    const saveBtnSelector = 'app-repeat-section-dialog .repeat-section-dialog-save';
    const numRepeats = await this.page.getElements('app-repeat-section').count();
    if (numRepeats > 0) {
      const repeatSections: ElementFinder[] = await this.page.getElements('app-repeat-section');
      for (const e of repeatSections) {
        const numDialogs = await this.page.getElements(dialogSelector).count();
        if (numDialogs > 0) {
          await expect(this.page.getElement(dialogSelector).isDisplayed()).toBeFalsy();
        } else {
          await expect(this.page.getElements(dialogSelector).count()).toEqual(0);
        }
        await expect(e.$$(itemSelector).count()).toEqual(0);
        await e.$('.repeat-action button').click();
        await this.page.waitForVisible(dialogSelector);
        await expect(this.page.getElement(dialogSelector).isDisplayed()).toBeTruthy();
        await this.page.waitFor(100);
        await this.fillOutRequiredFields(
          `${dialogSelector} .mat-form-field-required-marker`,
          `${saveBtnSelector}.disabled`,
          `${dialogSelector} .ng-invalid`,
          '#highlight-required-fields-in-dialog'
        );
        await this.page.waitFor(100).then(async () => {
          await this.page.waitForNotVisible(`${saveBtnSelector}.disabled`);
          await this.page.waitForClickable(saveBtnSelector);
          await this.page.waitFor(100);

          // Silly hack to force mat-dialog to notice click
          for (let i = 0; i < 10; i++) {
            const numDialogs2 = await this.page.getElements(dialogSelector).count();
            if (numDialogs2 > 0) {
              await this.page.waitFor(100);
              await this.page.clickElement(saveBtnSelector);
              await this.page.waitFor(100);
            } else {
              break;
            }
          }
          await this.page.waitForNotVisible(dialogSelector);
          await expect(e.$$(itemSelector).count()).toEqual(1);
          await expect(this.page.getElements(dialogSelector).count()).toEqual(0);
          await this.page.waitFor(100);
        });
      }
    }

    return expect(this.page.getElements(itemSelector).count()).toEqual(numRepeats);
  }
}
