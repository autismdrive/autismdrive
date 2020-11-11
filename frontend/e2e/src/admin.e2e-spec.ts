import {AppPage} from './app-page.po';
import {AdminUseCases} from './use-cases/admin.po';
import {EnrollUseCases} from './use-cases/enroll.po';
import {GlobalHeaderUseCases} from './use-cases/global-header.po';
import {LoginUseCases} from './use-cases/login.po';
import {ProfileUseCases} from './use-cases/profile.po';
import {SearchUseCases} from './use-cases/search.po';
import {StudiesUseCases} from './use-cases/studies.po';

describe('Admin', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let searchUseCases: SearchUseCases;
  let profileUseCases: ProfileUseCases;
  let enrollUseCases: EnrollUseCases;
  let adminUseCases: AdminUseCases;
  let studiesUseCases: StudiesUseCases;
  const email = 'eleanorcjkgraham@gmail.com';
  const password = 'Random Frequent Flyer Dent 34';

  beforeAll(async () => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    searchUseCases = new SearchUseCases(page);
    profileUseCases = new ProfileUseCases(page);
    enrollUseCases = new EnrollUseCases(page);
    adminUseCases = new AdminUseCases(page);
    studiesUseCases = new StudiesUseCases(page);
    await page.waitForAngularEnabled(true);
    await page.navigateToHome();
    await loginUseCases.refreshAndRedirectToReturnUrl();
  });

  afterAll(async () => {
    await page.waitForAngularEnabled(true);
  });

  // Login & Register
  it('should display login form', () => loginUseCases.displayLoginForm());
  it('should log in with email and password', () => loginUseCases.loginWithCredentials(email, password));

  // Global Header - Logged In
  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should display logged-in header state', () => globalHeaderUseCases.displayLoggedInState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());

  // Admin Screen
  it('should display admin link', () => globalHeaderUseCases.displayAdminLink());
  it('should navigate to admin screen', () => adminUseCases.navigateToAdmin());
  it('should navigate to user admin tab', () => adminUseCases.navigateToTab('#user-admin', '.users-table'));
  it('should navigate to participant admin tab', () => adminUseCases.navigateToTab('#participant-admin', '.participant-admin'));
  it('should navigate to taxonomy admin tab', () => adminUseCases.navigateToTab('#taxonomy-admin', '.taxonomy-admin'));
  it('should navigate to import/export status tab', () => adminUseCases.navigateToTab('#import-export-status', '.logs'));
  it('should navigate to email log tab', () => adminUseCases.navigateToTab('#email-log', '.email-log-admin'));
  it('should navigate to data admin tab', () => adminUseCases.navigateToTab('#data-admin', '.data-list'));
  it('should export all questionnaire data');
  it('should hide sensitive data');
  it('should display data table for each flow step');
  it('should navigate to user admin tab');
  it('should display user admin columns');
  it('should sort by user admin columns');
  it('should search users by id');
  it('should search users by email');
  it('should navigate to user detail page');
  it('should export user data');
  it('should display related participants');
  it('should display edit log');
  it('should display email log');

  // Study Form
  it('should visit home page', () => globalHeaderUseCases.visitHomePage());
  it('should navigate to the studies page', () => studiesUseCases.navigateToStudiesPage());
  it('should display the study add button', () => adminUseCases.viewAddButton());
  it('should click and open the study form', () => adminUseCases.openForm('.add-button', '/studies/add'));
  it('should fill out the required fields');
  it('should save and be directed to the study detail page');
  it('should display the study edit button');
  it('should click and open the study form');
  it('should edit required fields');
  it('should save and be directed to the study detail page');
  it('should click and open the study form');
  it('should delete and be directed to studies');


  // Log out
  it('should log out', () => loginUseCases.logout());
  it('should display logged-out header state', () => globalHeaderUseCases.displayLoggedOutState());
});
