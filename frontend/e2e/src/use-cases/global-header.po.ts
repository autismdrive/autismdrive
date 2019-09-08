import { AppPage } from '../app-page.po';

export class GlobalHeaderUseCases {
  constructor(private page: AppPage) {
  }

  displaySitewideHeader() {
    expect(this.page.getElements('#menu-bar').count()).toEqual(1);
    expect(this.page.getElements('app-logo').count()).toEqual(1);
    expect(this.page.getElements('#uva-header').count()).toEqual(1);
  }

  displayLoggedOutState() {
    expect(this.page.getElements('#register-button').count()).toEqual(1);
    expect(this.page.getElements('#login-button').count()).toEqual(1);
    expect(this.page.getElements('#profile-button').count()).toEqual(0);
    expect(this.page.getElements('#logout-button').count()).toEqual(0);
  }

  displayLoggedInState() {
    expect(this.page.getElements('#register-button').count()).toEqual(0);
    expect(this.page.getElements('#login-button').count()).toEqual(0);
    expect(this.page.getElements('#profile-button').count()).toEqual(1);
    expect(this.page.getElements('#logout-button').count()).toEqual(1);
  }

  displayPrimaryNav() {
    expect(this.page.getElements('#primary-nav').count()).toEqual(1);
    expect(this.page.getElements('#about-button').count()).toEqual(1);
    expect(this.page.getElements('#studies-button').count()).toEqual(1);
    expect(this.page.getElements('#resources-button').count()).toEqual(1);
  }

  visitHomePage() {
    this.page.clickLinkTo('/home');
    this.page.waitForVisible('app-news-item');
    expect(this.page.getElements('#hero').count()).toEqual(1);
    expect(this.page.getElements('.border-box-tile').count()).toBeGreaterThan(1);
    expect(this.page.getElements('app-news-item').count()).toBeGreaterThan(1);
  }

  async displayHomeHero() {
    const numSlides = await this.page.getElements('.hero-slides .hero-slide').count();

    for (let i = 0; i < numSlides; i++) {
      this.page.clickElement(`.hero-slides .dots .dot:nth-of-type(${i + 1})`);
      expect(this.page.getElements(`.hero-slides .hero-slide:nth-of-type(${i + 1}).active`).count()).toEqual(1);
    }
  }

  visitAboutPage() {
    this.page.clickLinkTo('/about');
    expect(this.page.getElements('.about').count()).toEqual(1);
    expect(this.page.getElements('#hero').count()).toEqual(1);
    expect(this.page.getElements('#feature').count()).toEqual(1);
    this.page.clickLinkTo('/home');
  }

  visitStudiesPage() {
    this.page.clickLinkTo('/studies');
    expect(this.page.getElements('.studies').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
    this.page.clickLinkTo('/home');
  }

  visitResourcesPage() {
    this.page.clickLinkTo('/search');
    this.page.waitForVisible('app-search-result');

    ['resource', 'location', 'event'].forEach(t => {
      expect(this.page.getElements(`app-border-box-tile .${t}`).count()).toEqual(1);
    });
    expect(this.page.getElements('agm-map').count()).toEqual(1);
    expect(this.page.getElements('app-search-result').count()).toBeGreaterThan(1);
    expect(this.page.getElements('.resource-gatherer').count()).toBeGreaterThan(1);
    this.page.clickLinkTo('/home');
  }
}
