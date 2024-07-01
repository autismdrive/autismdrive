/// <reference types="cypress" />
import {faker} from '@node_modules/@faker-js/faker';
import {AppPage} from '../support/util';
import {GlobalHeaderUseCases} from '../support/global-header';
import {LoginUseCases} from '../support/login';
import {SearchUseCases} from '../support/search';
import {StudiesUseCases} from '../support/studies';

describe('Anonymous User', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let searchUseCases: SearchUseCases;
  let studiesUseCases: StudiesUseCases;
  let randomEmail;

  before(() => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    searchUseCases = new SearchUseCases(page);
    studiesUseCases = new StudiesUseCases(page);
    randomEmail = faker.internet.email();
    page.waitForNetworkIdle();
    page.navigateToHome();
    page.waitForNetworkIdle();
    loginUseCases.refreshAndRedirectToReturnUrl();
  });

  after(() => {
    page.waitForNetworkIdle();
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
  it('should suggest categories when keywords entered in the search field', () =>
    searchUseCases.enterKeywordsInSearchField('ad'));
  it('should clear search filter', () => searchUseCases.removeFilter('topic', 'type'));
  it('should display results filtered by age', () => searchUseCases.displaySelectedCategory('age'));
  it('should sort results by distance from me', () => searchUseCases.sortByDistance());
  it('should allow user to set location via ZIP code', () => searchUseCases.enterZipCode('22101'));
  it('should display saved ZIP code', () => searchUseCases.checkSavedZipCode('22101'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should open ZIP code dialog again', () => searchUseCases.openZipCodeDialog());
  it('should change ZIP code', () => searchUseCases.enterZipCode('24248'));
  it('should display different saved ZIP code', () => searchUseCases.checkSavedZipCode('24248'));
  it('should display different results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should show all age ranges', () => searchUseCases.removeFilter('age', 'keyword'));
  it('should display only locations', () => searchUseCases.filterByType('location'));
  it('should display only online resources', () => searchUseCases.filterByType('resource'));
  it('should display only events', () => searchUseCases.filterByType('event'));
  it('should remove type filters when clicking All Resources tab', () => searchUseCases.filterByType('all'));
  it('should display only locations again', () => searchUseCases.filterByType('location'));
  it('should display results filtered by topic', () => searchUseCases.displaySelectedCategory('topic'));
  it('should preserve selected topic when removing type filter', () => searchUseCases.removeFilter('type', 'topic'));
  it('should sort results by last date updated', () => searchUseCases.sortByLastUpdated());
  it('should go back to home page', () => globalHeaderUseCases.visitHomePage());
  it('should return to the search page', () => globalHeaderUseCases.visitResourcesPage());
  it('should enter some other keywords in the search field', () =>
    searchUseCases.enterKeywordsInSearchField('staunton'));
  it('should clear the search box when leaving the search page', () => searchUseCases.clearSearchBox('staunton'));
  it('should display only events again', () => searchUseCases.filterByType('event'));
  it('should sort results by event date', () => searchUseCases.sortByEventDate());
  it('should display all resources again', () => searchUseCases.filterByType('all'));
  it('should display resource details and return to search when chip selected', () =>
    searchUseCases.displayResourceAndClickChip());
  it('should go back to the home page again', () => globalHeaderUseCases.visitHomePage());
  it('should go back to the search page again', () => globalHeaderUseCases.visitResourcesPage());
  it('should go to second page of results', () => searchUseCases.goToNextResultsPage());
  it('should display resource details', () => searchUseCases.displayResource());
  it('should go back to the second page of results', () => searchUseCases.goBackAndCheckPageNum());

  // Studies & study details
  it('should navigate to home page', () => globalHeaderUseCases.visitHomePage());
  it('should navigate to studies page', () => studiesUseCases.navigateToStudiesPage());
  it('should show currently-enrolling studies', () => studiesUseCases.filterByStatus('currently_enrolling'));
  it('should show studies in progress', () => studiesUseCases.filterByStatus('study_in_progress'));
  it('should show studies where results are being analyzed', () =>
    studiesUseCases.filterByStatus('results_being_analyzed'));
  it('should show studies that have been published', () => studiesUseCases.filterByStatus('study_results_published'));

  // Login & Register
  it('should jump back to the home page', () => globalHeaderUseCases.visitHomePage());
  it('should display login form', () => loginUseCases.displayLoginForm());
  it('should display forgot password form', () => loginUseCases.displayForgotPasswordForm());
  it('should display register form', () => loginUseCases.displayRegisterForm());
  it('should display confirmation message on submit', () => loginUseCases.displayRegisterConfirmation(randomEmail));
  it('should display error message when submitting a duplicate email address', () =>
    loginUseCases.displayRegisterError(randomEmail));
  it('should display Forgot Password form confirmation message', () =>
    loginUseCases.displayForgotPasswordConfirmation(randomEmail));
  it('should display Forgot Password form error message', () => loginUseCases.displayForgotPasswordError());
});
