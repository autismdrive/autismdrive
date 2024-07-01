/// <reference types="cypress" />
import {AppPage} from './util';

export class GlobalHeaderUseCases {
  constructor(private page: AppPage) {}

  displaySitewideHeader() {
    this.page.getElements('#menu-bar').should('have.length', 1);
    this.page.getElements('app-logo').should('have.length', 1);
  }

  displayLoggedOutState() {
    this.page.getElements('#register-button').should('have.length', 1);
    this.page.getElements('#login-button').should('have.length', 1);
    this.page.getElements('#profile-button').should('have.length', 0);
    this.page.getElements('#logout-button').should('have.length', 0);
  }

  displayLoggedInState() {
    this.page.getElements('#register-button').should('have.length', 0);
    this.page.getElements('#login-button').should('have.length', 0);
    this.page.getElements('#profile-button').should('have.length', 1);
    this.page.getElements('#logout-button').should('have.length', 1);
  }

  displayPrimaryNav() {
    this.page.getElements('#primary-nav').should('have.length', 1);
    this.page.getElements('#about-button').should('have.length', 1);
    this.page.getElements('#studies-button').should('have.length', 1);
    this.page.getElements('#resources-button').should('have.length', 1);
  }

  visitHomePage() {
    this.page.clickAndExpectRoute('#logo', '/home');
    this.page.waitForVisible('app-news-item');
    this.page.getElements('#hero').should('have.length', 1);
    this.page.getElements('.border-box-tile').should('have.length.gt', 1);
    this.page.getElements('app-news-item').should('have.length.gt', 1);
  }

  displayHomeHero() {
    const _page = this.page;
    _page.getElements('.hero-slides .hero-slide').each(function ($el, i) {
      _page.clickElement(`.hero-slides .dots .dot:nth-of-type(${i + 1})`);
      _page.getElements(`.hero-slides .hero-slide:nth-of-type(${i + 1}).active`).should('have.length', 1);
    });
  }

  visitAboutPage() {
    this.page.clickLinkTo('/about');
    this.page.getElements('.about').should('have.length', 1);
    this.page.getElements('#hero').should('have.length', 1);
    this.page.clickLinkTo('/home');
  }

  visitStudiesPage() {
    this.page.clickLinkTo('/studies');
    this.page.getElements('.studies').should('have.length', 1);
    this.page.getElements('app-search-result').should('have.length.gt', 1);
    this.page.clickLinkTo('/home');
  }

  visitResourcesPage() {
    this.page.clickLinkTo('/search');
    this.page.waitForVisible('app-search-result');

    ['resource', 'location', 'event'].forEach(t => {
      this.page.getElements(`.type-tabs .${t}`).should('have.length', 1);
    });

    this.page.getElements('app-search-result').should('have.length.gt', 1);
    this.page.getElements('.resource-gatherer').should('have.length.gt', 1);
  }

  checkForDoubleNavLabels() {
    this.page.resizeTo(1280, 720);
    this.page.getElements('#resources-button .mat-button-wrapper span').should('be.visible').should('have.length', 1);
    this.page.maximize();
  }

  displayAdminLink() {
    this.page.getElements('#admin-button').should('have.length', 1);
  }
}
