import { AppPage } from './app.po';

describe('Anonymous User', () => {
  let page: AppPage;
  let randomEmail;

  beforeAll(() => {
    page = new AppPage();
    randomEmail = `aaron_${page.getRandomString(16)}@sartography.com`;
    page.navigateToHome();
  });

  it('should display sitewide header', () => {
    expect(page.getElements('#menu-bar').count()).toEqual(1);
    expect(page.getElements('app-logo').count()).toEqual(1);
  });

  it('should display utility navigation', () => {
    expect(page.getElements('#utility-nav').count()).toEqual(1);
  });

  it('should display logged-out state in utility navigation', () => {
    expect(page.getElements('#register-button').count()).toEqual(1);
    expect(page.getElements('#login-button').count()).toEqual(1);
    expect(page.getElements('#profile-button').count()).toEqual(0);
    expect(page.getElements('#logout-button').count()).toEqual(0);
  });

  it('should display primary navigation', () => {
    expect(page.getElements('#primary-nav').count()).toEqual(1);
    expect(page.getElements('#enroll-button').count()).toEqual(1);
    expect(page.getElements('#studies-button').count()).toEqual(1);
    expect(page.getElements('#resources-button').count()).toEqual(1);
  });

  it('should display calls to action', () => {
    expect(page.getElements('#cta').count()).toEqual(1);
    expect(page.getElements('#cta button').count()).toBeGreaterThan(1);
  });

  it('should display enroll page', () => {
    page.clickLinkTo('/enroll');
    expect(page.getElements('.enroll').count()).toEqual(1);
    expect(page.getElements('#hero').count()).toEqual(1);
    expect(page.getElements('#feature').count()).toEqual(1);
    page.clickLinkTo('/home');
  });

  it('should display studies page', () => {
    page.clickLinkTo('/studies');
    expect(page.getElements('.studies').count()).toEqual(1);
    expect(page.getElements('app-filters').count()).toEqual(1);
    expect(page.getElements('app-search-result').count()).toBeGreaterThan(1);
    page.clickLinkTo('/home');
  });

  it('should display resources page', () => {
    page.clickLinkTo('/resources');
    expect(page.getElements('.resources').count()).toEqual(1);
    expect(page.getElements('app-filters').count()).toEqual(1);
    expect(page.getElements('app-search-result').count()).toBeGreaterThan(1);
    page.clickLinkTo('/home');
  });

  it('should display terms and conditions when Create Account button is clicked', () => {
    page.clickAndExpectRoute('#register-button', '/terms');
    expect(page.getElements('app-terms').count()).toEqual(1);
    expect(page.getElements('#agree').count()).toEqual(1);
    expect(page.getElements('#cancel').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

  it('should display login form', () => {
    page.waitForClickable('#login-button');
    page.clickElement('#login-button');
    expect(page.getElements('app-login').count()).toEqual(1);
    expect(page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(page.getElements('[id*="input_password"]').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

  it('should display forgot password form', () => {
    page.clickAndExpectRoute('#login-button', '/login');
    expect(page.getElements('app-login').count()).toEqual(1);
    page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    expect(page.getElements('app-forgot-password').count()).toEqual(1);
    expect(page.getElements('[id*="input_email"]').count()).toEqual(1);
    expect(page.getElements('[id*="input_password"]').count()).toEqual(0);
    expect(page.getElements('#cancel').count()).toEqual(1);
    expect(page.getElements('#submit').count()).toEqual(1);
    expect(page.getElements('#register').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

  it('should display register form', () => {
    page.clickAndExpectRoute('#login-button', '/login');
    expect(page.getElements('app-login').count()).toEqual(1);
    page.clickAndExpectRoute('#register', '/terms');
    expect(page.getElements('app-terms').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

  it('should accept terms and conditions', () => {
    page.clickAndExpectRoute('#login-button', '/login');
    expect(page.getElements('app-login').count()).toEqual(1);
    page.clickAndExpectRoute('#register', '/terms');
    expect(page.getElements('app-terms').count()).toEqual(1);
    page.clickAndExpectRoute('#agree', '/register');
  });

  it('should display confirmation message on submit', () => {
    page.inputText('[id*="input_email"]', randomEmail);
    page.clickElement('#submit');
    page.waitForNotVisible('app-loading');
    expect(page.getElements('#confirmation_message').count()).toEqual(1);
    expect(page.getElements('#error_message').count()).toEqual(0);
    page.clickAndExpectRoute('#continue', '/home');
  });

  it('should display error message when submitting a duplicate email address', () => {
    page.clickAndExpectRoute('#register-button', '/terms');
    expect(page.getElements('app-terms').count()).toEqual(1);
    page.clickAndExpectRoute('#agree', '/register');
    page.inputText('[id*="input_email"]', randomEmail);
    page.clickElement('#submit');
    page.waitForNotVisible('app-loading');
    expect(page.getElements('#confirmation_message').count()).toEqual(0);
    expect(page.getElements('#error_message').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

  it('should display confirmation message after submitting Forgot Password form', () => {
    page.clickAndExpectRoute('#login-button', '/login');
    page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    page.inputText('[id*="input_email"]', randomEmail);
    page.clickElement('#submit');
    page.waitForNotVisible('app-loading');
    expect(page.getElements('#confirmation_message').count()).toEqual(1);
    expect(page.getElements('#error_message').count()).toEqual(0);
    page.clickAndExpectRoute('#continue', '/home');
  });

  it('should display error message if submitting Forgot Password form for non-existent email', () => {
    const newRandomEmail = page.getRandomString(8) + '@' + page.getRandomString(8) + '.com';
    page.clickAndExpectRoute('#login-button', '/login');
    page.clickAndExpectRoute('#forgot_password', '/forgot-password');
    page.inputText('[id*="input_email"]', newRandomEmail);
    page.clickElement('#submit');
    page.waitForNotVisible('app-loading');
    expect(page.getElements('#confirmation_message').count()).toEqual(0);
    expect(page.getElements('#error_message').count()).toEqual(1);
    page.clickAndExpectRoute('#cancel', '/home');
  });

});
