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
    cy.get('#hero')
      .should('be.visible')
      .and('have.css', 'background-image', `url("http://localhost:4200/public/home/hero-family.jpg")`)
      .then($el => {
        const url = $el.css('background-image').match(/url\("(.*)"\)/)[1];
        cy.request({url, failOnStatusCode: false}).its('status').should('eq', 200);
      });
  }

  visitAboutPage() {
    this.page.clickLinkTo('/about');
    this.page.getElements('.about').should('have.length', 1);
    this.page.getElements('#hero').should('have.length', 1);
    this.page.clickLinkTo('/home');
  }

  visitStudiesPage() {
    this.page.clickLinkTo('/studies/currently_enrolling');
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
    this.page.getElements('#resources-button').should('be.visible').should('have.length', 1);
    this.page.maximize();
  }

  displayAdminLink() {
    this.page.getElements('#admin-button').should('have.length', 1);
  }
}
