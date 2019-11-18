import {AppPage} from './app-page.po';
import {GlobalHeaderUseCases} from './use-cases/global-header.po';
import {LoginUseCases} from './use-cases/login.po';
import {SearchUseCases} from './use-cases/search.po';
import {StudiesUseCases} from './use-cases/studies.po';

describe('Anonymous User', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let searchUseCases: SearchUseCases;
  let studiesUseCases: StudiesUseCases;
  let randomEmail;

  beforeAll(async () => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    searchUseCases = new SearchUseCases(page);
    studiesUseCases = new StudiesUseCases(page);
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
  it('should display selected category', () => searchUseCases.displaySelectedCategory('age'));
  it('should sort results by distance from me', () => searchUseCases.sortByDistance());
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should show all age ranges', () => searchUseCases.removeFilter('age', 'keyword'));
  it('should clear search keyword', () => searchUseCases.removeFilter('keyword', 'type'));
  it('should sort results by event date', () => searchUseCases.sortByEventDate());
  it('should display selected category', () => searchUseCases.displaySelectedCategory('topic'));
  it('should preserve selected topic when removing type filter', () => searchUseCases.removeFilter('type', 'topic'));
  it('should sort results by last date updated', () => searchUseCases.sortByLastUpdated());
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should go to search page when user presses enter in the search field', () => searchUseCases.enterKeywordsInSearchField());
  it('should clear the search box when leaving the search page', () => searchUseCases.clearSearchBox());

  // Resource details returns to search
  it('should visit search page', () => globalHeaderUseCases.visitResourcesPage());
  it('should display resource details and return to search when chip selected', () => searchUseCases.displayResourceAndClickChip());

  // Studies & study details
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should navigate to studies page', () => studiesUseCases.navigateToStudiesPage());
  it('should show currently-enrolling studies', () => studiesUseCases.filterByStatus('currently_enrolling'));
  it('should show studies in progress', () => studiesUseCases.filterByStatus('study_in_progress'));
  it('should show studies where results are being analyzed', () => studiesUseCases.filterByStatus('results_being_analyzed'));
  it('should show studies that have been published', () => studiesUseCases.filterByStatus('study_results_published'));

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
