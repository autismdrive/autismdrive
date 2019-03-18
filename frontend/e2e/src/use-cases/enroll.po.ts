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
      this.page.waitForAnimations();
      expect(this.page.getElement('form h1').getText()).toEqual(link.getText());
      expect(this.page.getElements('form mat-form-field').count()).toBeGreaterThan(0);
    });
  }
}
