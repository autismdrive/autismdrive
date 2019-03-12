import { AppPage } from './app.po';

describe('Anonymous User', () => {
  let page: AppPage;

  beforeAll(() => {
    page = new AppPage();
    page.navigateToHome();
  });

  it('should display sitewide header', () => {
    expect(page.getElements('#menu-bar').count()).toEqual(1);
    expect(page.getElements('app-logo').count()).toEqual(1);
  });

  it('should display utility navigation', () => {
    expect(page.getElements('#utility-nav').count()).toEqual(1);
  });

  it('should display logged-out state in utility navigation', () => {
    expect(page.getElements('#register-button').count()).toEqual(1);
    expect(page.getElements('#login-button').count()).toEqual(1);
    expect(page.getElements('#profile-button').count()).toEqual(0);
    expect(page.getElements('#logout-button').count()).toEqual(0);
  });

  it('should display primary navigation', () => {
    expect(page.getElements('#primary-nav').count()).toEqual(1);
    expect(page.getElements('#enroll-button').count()).toEqual(1);
    expect(page.getElements('#studies-button').count()).toEqual(1);
    expect(page.getElements('#resources-button').count()).toEqual(1);
  });

  it('should display calls to action', () => {
    expect(page.getElements('#cta').count()).toEqual(1);
    expect(page.getElements('#cta button').count()).toBeGreaterThan(1);
  });



});
