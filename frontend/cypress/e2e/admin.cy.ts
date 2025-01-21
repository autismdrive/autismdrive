/// <reference types="cypress" />
import {faker} from '@faker-js/faker';
import * as assert from 'node:assert';
import {AdminUseCases} from '../support/admin';
import {GlobalHeaderUseCases} from '../support/global-header';
import {LoginUseCases} from '../support/login';
import {StudiesUseCases} from '../support/studies';
import {AppPage} from '../support/util';

describe('Admin', () => {
  let page: AppPage;
  let globalHeaderUseCases: GlobalHeaderUseCases;
  let loginUseCases: LoginUseCases;
  let adminUseCases: AdminUseCases;
  let studiesUseCases: StudiesUseCases;

  const adminEmail = 'ajlouie@gmail.com';
  const adminPassword = faker.internet.password({
    length: 25,
    pattern: /[\dA-Za-z,.!@#$%^&*()_+-=;:'"<>?/\\`~|]/,
  });

  before(() => {
    page = new AppPage();
    globalHeaderUseCases = new GlobalHeaderUseCases(page);
    loginUseCases = new LoginUseCases(page);
    adminUseCases = new AdminUseCases(page);
    studiesUseCases = new StudiesUseCases(page);
    page.waitForNetworkIdle();
    page.navigateToHome();
    loginUseCases.refreshAndRedirectToReturnUrl();
  });

  after(() => {
    page.waitForNetworkIdle();
  });

  // Login & Register
  it('should display login form', () => loginUseCases.displayLoginForm());

  it('should navigate to login form again', () => {
    cy.log(`adminEmail = ${adminEmail}`);
    page.clickAndExpectRoute('#login-button', '/login');
  });

  it('should click forgot password button', () => {
    page.clickAndExpectRoute('#forgot_password', '/forgot-password');
  });

  it('should enter admin email', () => {
    cy.get('input[type="email"]').as('email-input');
    cy.get('@email-input').type(adminEmail);
    cy.get('@email-input').should('have.value', adminEmail);
    cy.get('#submit').click();
  });

  it('should get token URL', () => {
    // Get token URL from local storage
    cy.log(`localStorage.token_url = ${window.localStorage.getItem('token_url')}`);
  });

  it('should really get token URL', () => {
    cy.window()
      .its('localStorage')
      .invoke('getItem', 'token_url')
      .should('not.be.empty')
      .then(u => {
        cy.log(`token URL = ${u}`);
      });
  });

  it('should go to token URL', () => {
    // Get token URL from local storage
    page.getLocalStorageVar('token_url').then(u => {
      cy.visit(u);
    });
  });

  it('should reset admin password', () => {
    cy.get('input[type="password"]').first().type(adminPassword);
    cy.get('input[type="password"]').last().type(adminPassword);
    page.clickAndExpectRoute('#submit', '/profile');
  });

  it('should log out', () => loginUseCases.logout());

  it('should log in with email and password', () => loginUseCases.loginWithCredentials(adminEmail, adminPassword));

  // Global Header - Logged In
  it('should display sitewide header', () => globalHeaderUseCases.displaySitewideHeader());
  it('should display logged-in header state', () => globalHeaderUseCases.displayLoggedInState());
  it('should display primary navigation', () => globalHeaderUseCases.displayPrimaryNav());

  // Admin Screen
  it('should display admin link', () => globalHeaderUseCases.displayAdminLink());
  it('should navigate to admin screen', () => adminUseCases.navigateToAdmin());
  it('should navigate to user admin tab', () => adminUseCases.navigateToTab('#user-admin', '.users-table'));
  it('should navigate to participant admin tab', () =>
    adminUseCases.navigateToTab('#participant-admin', '.participant-admin'));
  it('should navigate to taxonomy admin tab', () => adminUseCases.navigateToTab('#taxonomy-admin', '.taxonomy-admin'));
  it('should navigate to import/export status tab', () =>
    adminUseCases.navigateToTab('#import-export-status', '.logs'));
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
  it('should log out again', () => loginUseCases.logout());
  it('should display logged-out header state', () => globalHeaderUseCases.displayLoggedOutState());
});
