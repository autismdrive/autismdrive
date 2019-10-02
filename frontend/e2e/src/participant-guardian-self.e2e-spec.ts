import { AppPage } from './app-page.po';
import { GlobalHeaderUseCases } from './use-cases/global-header.po';
import { LoginUseCases } from './use-cases/login.po';
import { ProfileUseCases } from './use-cases/profile.po';
import { EnrollUseCases } from './use-cases/enroll.po';
import { SearchUseCases } from './use-cases/search.po';

describe('Participant (Guardian - Self)', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let searchUseCases: SearchUseCases;
  let profileUseCases: ProfileUseCases;
  let enrollUseCases: EnrollUseCases;
  let randomEmail;
  const email = 'aaron@sartography.com';
  const password = 'Zarquon Disaster Area 78';

  beforeAll(async () => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    searchUseCases = new SearchUseCases(page);
    profileUseCases = new ProfileUseCases(page);
    enrollUseCases = new EnrollUseCases(page);
    randomEmail = `aaron_${page.getRandomString(16)}@sartography.com`;
    await page.waitForAngularEnabled(true);
    await page.navigateToHome();
  });

  afterAll(async () => {
    await page.waitForAngularEnabled(true);
  });

  // Login & Register
  it('should display login form', () => loginUseCases.displayLoginForm());
  it('should display forgot password form', () => loginUseCases.displayForgotPasswordForm());
  it('should display register form', () => loginUseCases.displayRegisterForm());
  it('should display confirmation message on submit', () => loginUseCases.displayRegisterConfirmation(randomEmail));
  it('should display error message when submitting a duplicate email address', () => loginUseCases.displayRegisterError(randomEmail));
  it('should display Forgot Password form confirmation message', () => loginUseCases.displayForgotPasswordConfirmation(randomEmail));
  it('should display Forgot Password form error message', () => loginUseCases.displayForgotPasswordError());
  it('should see error on bad password', () => loginUseCases.loginWithBadPassword(email));
  it('should log in with email and password', () => loginUseCases.loginWithCredentials(email, password));
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should stay on the profile screen on refresh', () => loginUseCases.refreshAndRedirectToReturnUrl());

  // Global Header - Logged In
  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should display logged-in header state', () => globalHeaderUseCases.displayLoggedInState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should display a sliding hero image', () => globalHeaderUseCases.displayHomeHero());
  it('should visit about page', () => globalHeaderUseCases.visitAboutPage());
  it('should visit studies page', () => globalHeaderUseCases.visitStudiesPage());
  it('should visit resources page', () => globalHeaderUseCases.visitResourcesPage());

  // Profile
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should display profile screen', () => profileUseCases.displayProfileScreen());
  it('should start Guardian flow when enrolling a dependent', () => profileUseCases.startGuardianFlow());
  it('should display the terms of consent to the study', () => enrollUseCases.displayGuardianTerms());
  it('should cancel out of the terms consent page', () => enrollUseCases.cancelTerms());
  it('should navigate back to the Guardian flow', () => profileUseCases.startGuardianFlow());
  it('should accept the terms', () => enrollUseCases.acceptTerms());
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should start the Dependent flow', () => profileUseCases.startDependentFlow());
  it('should accept the terms', () => enrollUseCases.acceptTerms());
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should display avatars for each participant', () => profileUseCases.displayAvatars());
  it('should display the avatar selection dialog', () => profileUseCases.displayAvatarDialog());
  it('should edit the avatar image', () => profileUseCases.editAvatarImg());
  it('should edit the avatar color', () => profileUseCases.editAvatarColor());
  it('should save changes to the avatar', () => profileUseCases.saveAvatar());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());

  // Enrollment Flow
  it('should display a menu link to all steps of the flow', () => enrollUseCases.displayMenuLinks());
  it('should display completed status of each step', () => enrollUseCases.displayCompletedStatus());
  it('should cancel enrollment instructions', () => enrollUseCases.cancelIntro());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());
  it('should navigate to each step of the flow', () => enrollUseCases.navigateToEachStep());
  it('should cancel editing enrollment info', () => enrollUseCases.cancelEditing());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());
  it('should display instructions for the entire flow', () => enrollUseCases.displayInstructions());
  it('should complete Guardian Identification step', () => enrollUseCases.completeStep(0));
  it('should complete Guardian Contact Information step', () => enrollUseCases.completeStep(1));
  it('should complete Guardian Demographics step', () => enrollUseCases.completeStep(2));
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should navigate back to the Dependent flow', () => profileUseCases.navigateToDependentFlow());
  it('should display instructions for the entire flow', () => enrollUseCases.displayInstructions());
  it('should complete Dependent Identification step', () => enrollUseCases.completeStep(0));
  it('should complete Dependent Demographics step', () => enrollUseCases.completeStep(1));
  it('should complete Dependent Home step', () => enrollUseCases.completeStep(2));
  it('should complete Dependent Evaluation History step', () => enrollUseCases.completeStep(3));
  it('should complete Dependent Clinical Diagnosis step', () => enrollUseCases.completeStep(4));
  it('should complete Dependent Birth and Developmental History step', () => enrollUseCases.completeStep(5));
  it('should complete Dependent Current Behaviors step', () => enrollUseCases.completeStep(6));
  it('should complete Dependent Education step', () => enrollUseCases.completeStep(7));
  it('should complete Dependent Supports step', () => enrollUseCases.completeStep(8));
  it('should navigate to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should allow user to view/edit non-sensitive responses');
  it('should not allow user to view or edit sensitive responses');

  // Search - Logged In
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should go to search page when user presses enter in the search field', () => searchUseCases.enterKeywordsInSearchField());
  it('should display selected category', () => searchUseCases.displaySelectedCategory('age'));
  it('should sort results by distance from me', () => searchUseCases.sortByDistance());
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should open ZIP code dialog', () => searchUseCases.openZipCodeDialog());
  it('should allow user to set location via ZIP code', () => searchUseCases.enterZipCode('22101'));
  it('should display saved ZIP code', () => searchUseCases.checkSavedZipCode('22101'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should open ZIP code dialog again', () => searchUseCases.openZipCodeDialog());
  it('should change ZIP code', () => searchUseCases.enterZipCode('24248'));
  it('should display saved ZIP code', () => searchUseCases.checkSavedZipCode('24248'));
  it('should display results in order by distance', () => searchUseCases.checkResultsDistance());
  it('should allow user to use GPS for location instead, clearing the stored ZIP code', () => searchUseCases.clearZipCode('24248'));
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

  // Log out
  it('should log out', () => loginUseCases.logout());
  it('should display logged-out header state', () => globalHeaderUseCases.displayLoggedOutState());
});
