import { AppPage } from './app-page.po';
import { GlobalHeaderUseCases } from './use-cases/global-header.po';
import { LoginUseCases } from './use-cases/login.po';
import { ProfileUseCases } from './use-cases/profile.po';
import { EnrollUseCases } from './use-cases/enroll.po';

describe('Participant (Guardian - Self)', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let profileUseCases: ProfileUseCases;
  let enrollUseCases: EnrollUseCases;
  let randomEmail;
  const email = 'aaron@sartography.com';
  const password = 'alouie3';

  beforeAll(() => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    profileUseCases = new ProfileUseCases(page);
    enrollUseCases = new EnrollUseCases(page);
    randomEmail = `aaron_${page.getRandomString(16)}@sartography.com`;
    page.navigateToHome();
  });

  // Global Header
  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should display utility navigation', () => globalHeaderUseCases.displayUtilityNav());
  it('should display logged-out state in utility navigation', () => globalHeaderUseCases.displayLoggedOutState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should display a sliding hero image', () => globalHeaderUseCases.displayHomeHero());
  it('should visit enroll page', () => globalHeaderUseCases.visitEnrollPage());
  it('should visit studies page', () => globalHeaderUseCases.visitStudiesPage());
  it('should visit resources search page', () => globalHeaderUseCases.visitResourcesSearchPage());

  // Login & Register
  it('should display login form', () => loginUseCases.displayLoginForm());
  it('should display forgot password form', () => loginUseCases.displayForgotPasswordForm());
  it('should display register form', () => loginUseCases.displayRegisterForm());
  it('should display confirmation message on submit', () => loginUseCases.displayRegisterConfirmation(randomEmail));
  it('should display error message when submitting a duplicate email address', () => loginUseCases.displayRegisterError(randomEmail));
  it('should display Forgot Password form confirmation message', () => loginUseCases.displayForgotPasswordConfirmation(randomEmail));
  it('should display Forgot Password form error message', () => loginUseCases.displayForgotPasswordError());
  it('should log in with email and password', () => loginUseCases.loginWithCredentials(email, password));
  it('should display logged-in header state', () => globalHeaderUseCases.displayLoggedInState());

  // Profile
  it('should display profile screen', () => profileUseCases.displayProfileScreen());
  it('should start Guardian flow when enrolling a dependent', () => profileUseCases.startGuardianFlow());
  it('should navigate back to the Profile screen', () => profileUseCases.navigateToProfile());
  it('should display avatars for each participant', () => profileUseCases.displayAvatars());
  it('should display the avatar selection dialog', () => profileUseCases.displayAvatarDialog());
  it('should edit the avatar image', () => profileUseCases.editAvatarImg());
  it('should edit the avatar color', () => profileUseCases.editAvatarColor());
  it('should save changes to the avatar', () => profileUseCases.saveAvatar());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());

  // Enrollment Flow
  it('should display the terms of consent to the study', () => enrollUseCases.displayTerms());
  it('should cancel out of the terms consent page', () => enrollUseCases.cancelEditing());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());
  it('should accept the terms', () => enrollUseCases.acceptTerms());
  it('should display a menu link to all steps of the flow', () => enrollUseCases.displayMenuLinks());
  it('should display completed status of each step', () => enrollUseCases.displayCompletedStatus());
  it('should navigate to each step of the flow', () => enrollUseCases.navigateToEachStep());
  it('should cancel editing enrollment info', () => enrollUseCases.cancelEditing());
  it('should navigate back to the Guardian flow', () => profileUseCases.navigateToGuardianFlow());
  it('should display instructions for the entire flow', () => enrollUseCases.displayInstructions());
  it('should fill out the required fields for each step', () => enrollUseCases.fillOutRequiredFields());
  it('should check off steps as complete');
  it('should display progress on the Profile screen');
  it('should allow user to view/edit non-sensitive responses');
  it('should not allow user to view or edit sensitive responses');

  // Log out
  it('should log out', () => loginUseCases.logout());
  it('should display logged-out header state', () => globalHeaderUseCases.displayLoggedOutState());
});
