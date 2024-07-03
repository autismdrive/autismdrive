/// <reference types="cypress" />
import {AppPage} from './util';

export class LoginUseCases {
  constructor(private page: AppPage) {}

  displayLoginForm() {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    this.page.getElements('app-login').should('have.length', 1);
    this.page.getElements('[id*="input_email"]').should('have.length', 1);
    this.page.getElements('[id*="input_password"]').should('have.length', 1);
    this.page.clickAndExpectRoute('#cancel', '#/home');
  }

  displayForgotPasswordForm() {
    this.page.clickAndExpectRoute('#login-button', '#/login');
    this.page.getElements('app-login').should('have.length', 1);
    this.page.clickAndExpectRoute('#forgot_password', '#/forgot-password');
    this.page.getElements('app-forgot-password').should('have.length', 1);
    this.page.getElements('[id*="input_email"]').should('have.length', 1);
    this.page.getElements('[id*="input_password"]').should('have.length', 0);
    this.page.getElements('#cancel').should('have.length', 1);
    this.page.getElements('#submit').should('have.length', 1);
    this.page.getElements('#register').should('have.length', 1);
    this.page.clickAndExpectRoute('#cancel', '#/home');
  }

  displayRegisterForm() {
    this.page.clickAndExpectRoute('#login-button', '#/login');
    this.page.getElements('app-login').should('have.length', 1);
    this.page.clickAndExpectRoute('#register', '#/register');
    this.page.getElements('app-register').should('have.length', 1);
  }

  displayRegisterConfirmation(email: string) {
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    this.page.waitForVisible('#confirmation_message');
    this.page.getElements('#confirmation_message').should('have.length', 1);
    this.page.getElements('#error_message').should('have.length', 0);
    this.page.clickAndExpectRoute('#continue', '#/home');
  }

  displayResetPasswordForm() {
    const _page = this.page;
    _page
      .getLocalStorageVar('token_url')
      .should('not.be.empty')
      .then(function (tokenUrl) {
        _page.navigateToUrl(tokenUrl.toString());
      });
  }

  displayErrorOnInsecurePassword(badPassword: string) {
    const errorSelector = 'formly-field.password .mat-error formly-validation-message';
    this.page.inputText('formly-field.password input', badPassword, true);
    this.page.waitForVisible(errorSelector);
    this.page.getElements(errorSelector).should('have.length', 1);
    this.page.getElement(errorSelector).should('contain.text', 'Your password must be at least');
  }

  fillOutPasswordForm(goodPassword: string) {
    this.page.inputText('formly-field.password input', goodPassword, true);
    this.page.getElements('.mat-error').should('have.length', 0);
  }

  submitResetPasswordForm(password: string) {
    this.page.inputText('formly-field.password input', password, true);
    this.page.inputText('formly-field.passwordConfirm input', password, true);
    this.page.getElements('.mat-error').should('have.length', 0);
    this.page.clickAndExpectRoute('#submit', '#/profile');
  }

  displayRegisterError(email: string) {
    this.page.clickAndExpectRoute('#register-button', '#/register');
    this.page.getElements('app-register').should('have.length', 1);
    this.page.inputText('[id*="input_email"]', email, true);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    this.page.getElements('#confirmation_message').should('have.length', 0);
    this.page.getElements('#error_message').should('have.length', 1);
    this.page.getElement('#error_message').should('have.text', 'The email you provided is already in use.');
    this.page.clickAndExpectRoute('#cancel', '#/home');
  }

  displayForgotPasswordConfirmation(email: string) {
    this.page.clickAndExpectRoute('#login-button', '#/login');
    this.page.clickAndExpectRoute('#forgot_password', '#/forgot-password');
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    this.page.getElements('#confirmation_message').should('have.length', 1);
    this.page.getElements('#error_message').should('have.length', 0);
    this.page.clickAndExpectRoute('#continue', '#/home');
  }

  displayForgotPasswordError() {
    const nonExistentEmail = this.page.getRandomString(8) + '@' + this.page.getRandomString(8) + '.com';
    this.page.clickAndExpectRoute('#login-button', '#/login');
    this.page.clickAndExpectRoute('#forgot_password', '#/forgot-password');
    this.page.inputText('[id*="input_email"]', nonExistentEmail);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    this.page.getElements('#confirmation_message').should('have.length', 0);
    this.page.getElements('#error_message').should('have.length', 1);
    this.page.clickAndExpectRoute('#cancel', '#/home');
  }

  loginWithBadPassword(email: string, badPassword: string) {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    this.page.getElements('app-login').should('have.length', 1);
    this.page.getElements('[id*="input_email"]').should('have.length', 1);
    this.page.getElements('[id*="input_password"]').should('have.length', 1);
    this.page.inputText('[id*="input_email"]', email);
    this.page.inputText('[id*="input_password"]', badPassword);
    this.page.clickAndExpectRoute('#submit', '#/login');
    this.page.getElements('#error_message').should('have.length', 1);
    this.page.getElement('#error_message').should('have.text', 'The credentials you supplied are incorrect.');
  }

  loginWithCredentials(email: string, password: string) {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    this.page.getElements('app-login').should('have.length', 1);
    this.page.getElement('[id*="input_email"]').clear();
    this.page.getElement('[id*="input_password"]').clear();
    this.page.getElements('[id*="input_email"]').should('have.length', 1);
    this.page.getElements('[id*="input_password"]').should('have.length', 1);
    this.page.inputText('[id*="input_email"]', email);
    this.page.inputText('[id*="input_password"]', password);
    this.page.clickAndExpectRoute('#submit', '#/profile');
  }

  logout() {
    this.page.waitForClickable('#logout-button');
    this.page.clickElement('#logout-button');
    this.page.getElements('app-logout').should('have.length', 1);
    this.page.clickAndExpectRoute('#ok-button', '#/home');
  }

  refreshAndRedirectToReturnUrl() {
    cy.location('hash').as('previousRoute');
    cy.reload();
    cy.waitForNetworkIdle(3000);
    cy.location('hash').should(function (route) {
      expect(route).to.eq(this.previousRoute);
    });
  }
}
