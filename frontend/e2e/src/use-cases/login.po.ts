import { AppPage } from '../app-page.po';

export class LoginUseCases {
  constructor(private page: AppPage) {
  }

  displayTerms() {
    this.page.clickAndExpectRoute('#register-button', '/terms');
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    expect(this.page.getElements('#agree').count()).toEqual(1);
    expect(this.page.getElements('#cancel').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

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
    this.page.clickAndExpectRoute('#register', '/terms');
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    this.page.clickAndExpectRoute('#cancel', '/home');
  }

  acceptTerms() {
    this.page.clickAndExpectRoute('#login-button', '/login');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    this.page.clickAndExpectRoute('#register', '/terms');
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    this.page.clickAndExpectRoute('#agree', '/register');
  }

  displayRegisterConfirmation(email: string) {
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(1);
    expect(this.page.getElements('#error_message').count()).toEqual(0);
    this.page.clickAndExpectRoute('#continue', '/home');
  }

  displayRegisterError(email: string) {
    this.page.clickAndExpectRoute('#register-button', '/terms');
    expect(this.page.getElements('app-terms').count()).toEqual(1);
    this.page.clickAndExpectRoute('#agree', '/register');
    this.page.inputText('[id*="input_email"]', email);
    this.page.clickElement('#submit');
    this.page.waitForNotVisible('app-loading');
    expect(this.page.getElements('#confirmation_message').count()).toEqual(0);
    expect(this.page.getElements('#error_message').count()).toEqual(1);
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

  loginWithCredentials(email: string, password: string) {
    this.page.waitForClickable('#login-button');
    this.page.clickElement('#login-button');
    expect(this.page.getElements('app-login').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(this.page.getElements('[id*="input_password"]').count()).toEqual(1);
    this.page.inputText('[id*="input_email"]', email);
    this.page.inputText('[id*="input_password"]', password);
    this.page.clickAndExpectRoute('#submit', '/profile');
    expect(this.page.getElements('app-profile').count()).toEqual(1);
    expect(this.page.getElements('#enroll_self').count()).toEqual(1);
    expect(this.page.getElements('#enroll_guardian').count()).toEqual(1);
    expect(this.page.getElements('#enroll_professional').count()).toEqual(1);
  }
}
