/// <reference types="cypress" />
import {AppPage} from './util';

export class LoginUseCases {
  constructor(private page: AppPage) {}

  displayLoginForm() {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_password"]').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

  displayForgotPasswordForm() {
    this.page.clickAndExpectRoute('#login-button', '/login');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    this.page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    expect(this.page.getElements('app-forgot-password').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_password"]').count()).toEqual(0);
    expect(this.page.getElements('#cancel').count()).toEqual(1);
    expect(this.page.getElements('#submit').count()).toEqual(1);
    expect(this.page.getElements('#register').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

  displayRegisterForm() {
    this.page.clickAndExpectRoute('#login-button', '/login');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    this.page.clickAndExpectRoute('#register', '/register');
    expect(this.page.getElements('app-register').count()).toEqual(1);
  }

  displayRegisterConfirmation(email: string) {
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    this.page.waitForVisible('#confirmation_message');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(1);
    expect(this.page.getElements('#error_message').count()).toEqual(0);
    this.page.clickAndExpectRoute('#continue', '/home');
  }

  async displayResetPasswordForm() {
    const tokenUrl = await this.page.getLocalStorageVar('token_url');
    expect(tokenUrl).toBeTruthy();
    this.page.navigateToUrl(tokenUrl.toString());
  }

  async displayErrorOnInsecurePassword(badPassword: string) {
    const errorSelector = 'formly-field.password .mat-error formly-validation-message';
    await this.page.inputText('formly-field.password input', badPassword, true);
    await this.page.waitForVisible(errorSelector);
    const numErrors = await this.page.getElements(errorSelector).count();
    expect(numErrors).toEqual(1);

    const errorText = await this.page.getElement(errorSelector).getText();
    expect(errorText).toContain('Your password must be at least');
  }

  fillOutPasswordForm(goodPassword: string) {
    this.page.inputText('formly-field.password input', goodPassword, true);
    expect(this.page.getElements('.mat-error').count()).toEqual(0);
  }

  submitResetPasswordForm(password: string) {
    this.page.inputText('formly-field.password input', password, true);
    this.page.inputText('formly-field.passwordConfirm input', password, true);
    expect(this.page.getElements('.mat-error').count()).toEqual(0);
    this.page.clickAndExpectRoute('#submit', '/profile');
  }

  displayRegisterError(email: string) {
    this.page.clickAndExpectRoute('#register-button', '/register');
    expect(this.page.getElements('app-register').count()).toEqual(1);
    this.page.inputText('[id*="input_email"]', email, true);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(0);
    expect(this.page.getElements('#error_message').count()).toEqual(1);
    expect(this.page.getElement('#error_message').getText()).toEqual('The email you provided is already in use.');
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

  displayForgotPasswordConfirmation(email: string) {
    this.page.clickAndExpectRoute('#login-button', '/login');
    this.page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(1);
    expect(this.page.getElements('#error_message').count()).toEqual(0);
    this.page.clickAndExpectRoute('#continue', '/home');
  }

  displayForgotPasswordError() {
    const nonExistentEmail = this.page.getRandomString(8) + '@' + this.page.getRandomString(8) + '.com';
    this.page.clickAndExpectRoute('#login-button', '/login');
    this.page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    this.page.inputText('[id*="input_email"]', nonExistentEmail);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(0);
    expect(this.page.getElements('#error_message').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

  loginWithBadPassword(email: string) {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_password"]').count()).toEqual(1);
    this.page.inputText('[id*="input_email"]', email);
    this.page.inputText('[id*="input_password"]', 'not a valid password');
    this.page.clickAndExpectRoute('#submit', '/login');
    expect(this.page.getElements('#error_message').count()).toEqual(1);
    expect(this.page.getElement('#error_message').getText()).toEqual('The credentials you supplied are incorrect.');
  }

  loginWithCredentials(email: string, password: string) {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    this.page.getElement('[id*="input_email"]').clear();
    this.page.getElement('[id*="input_password"]').clear();
    expect(this.page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_password"]').count()).toEqual(1);
    this.page.inputText('[id*="input_email"]', email);
    this.page.inputText('[id*="input_password"]', password);
    this.page.clickAndExpectRoute('#submit', '/profile');
  }

  logout() {
    this.page.waitForClickable('#logout-button');
    this.page.clickElement('#logout-button');
    expect(this.page.getElements('app-logout').count()).toEqual(1);
    this.page.clickAndExpectRoute('#ok-button', '/home');
  }

  async refreshAndRedirectToReturnUrl() {
    const previousRoute = this.page.getRoute();
    this.page.refresh().then(() => expect(this.page.getRoute()).toEqual(previousRoute));
  }
}
