import { AppPage } from './app-page.po';
import { GlobalHeaderUseCases } from './use-cases/global-header.po';
import { LoginUseCases } from './use-cases/login.po';
import { SearchUseCases } from './use-cases/search.po';

describe('Anonymous User', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let searchUseCases: SearchUseCases;
  let randomEmail;

  beforeAll(async () => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    searchUseCases = new SearchUseCases(page);
    randomEmail = `aaron_${page.getRandomString(16)}@sartography.com`;
    await page.waitForAngularEnabled(true);
    await page.navigateToHome();
  });

  afterAll(async () => {
    await page.waitForAngularEnabled(true);
  });

  // Global Header
  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should not display double nav labels', () => globalHeaderUseCases.checkForDoubleNavLabels());
  it('should stay on the home page on refresh', () => loginUseCases.refreshAndRedirectToReturnUrl());
  it('should display logged-out state in navigation', () => globalHeaderUseCases.displayLoggedOutState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should display a sliding hero image', () => globalHeaderUseCases.displayHomeHero());
  it('should visit about page', () => globalHeaderUseCases.visitAboutPage());
  it('should visit studies page', () => globalHeaderUseCases.visitStudiesPage());
  it('should visit resources page', () => globalHeaderUseCases.visitResourcesPage());

  // Search
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should go to search page when user presses enter in the search field', () => searchUseCases.enterKeywordsInSearchField());
  it('should display selected category', () => searchUseCases.displaySelectedCategory());
  it('should sort results by distance from user location', () => searchUseCases.sortByDistance());
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should open ZIP code ZIP code dialog', () => searchUseCases.openZipCodeDialog());
  it('should allow user to set location via ZIP code', () => searchUseCases.enterZipCode('22101'));
  it('should display saved ZIP code', () => searchUseCases.checkSavedZipCode('22101'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should open ZIP code dialog again', () => searchUseCases.openZipCodeDialog());
  it('should change ZIP code', () => searchUseCases.enterZipCode('24248'));
  it('should display saved ZIP code', () => searchUseCases.checkSavedZipCode('24248'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should allow user to use GPS for location instead, clearing the stored ZIP code', () => searchUseCases.clearZipCode('24248'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should sort by last date updated');
  it('should clear the search box when leaving the search page', () => searchUseCases.clearSearchBox());

  // Login & Register
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should display login form', () => loginUseCases.displayLoginForm());
  it('should display forgot password form', () => loginUseCases.displayForgotPasswordForm());
  it('should display register form', () => loginUseCases.displayRegisterForm());
  it('should display confirmation message on submit', () => loginUseCases.displayRegisterConfirmation(randomEmail));
  it('should display error message when submitting a duplicate email address', () => loginUseCases.displayRegisterError(randomEmail));
  it('should display Forgot Password form confirmation message', () => loginUseCases.displayForgotPasswordConfirmation(randomEmail));
  it('should display Forgot Password form error message', () => loginUseCases.displayForgotPasswordError());
});
