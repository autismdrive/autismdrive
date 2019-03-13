import { AppPage } from './app-page.po';
import { GlobalHeaderUseCases } from './use-cases/global-header.po';

describe('Participant (Guardian - Self)', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let randomEmail;

  beforeAll(() => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    randomEmail = `aaron_${page.getRandomString(16)}@sartography.com`;
    page.navigateToHome();
  });

  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should display utility navigation', () => globalHeaderUseCases.displayUtilityNav());
  it('should display logged-out state in utility navigation', () => globalHeaderUseCases.displayLoggedOutState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should visit enroll page', () => globalHeaderUseCases.visitEnrollPage());
  it('should visit studies page', () => globalHeaderUseCases.visitStudiesPage());
  it('should visit resources page', () => globalHeaderUseCases.visitResourcesPage());

  // Login
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
