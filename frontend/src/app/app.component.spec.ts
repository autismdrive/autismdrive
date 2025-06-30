import {signal} from '@angular/core';
import {TestBed} from '@angular/core/testing';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockAppEnvironment} from '@app/shared/fixtures/mock-app-environment';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {AppComponent} from './app.component';

describe('AppComponent', () => {
  let fixture: MockedComponentFixture<AppComponent>;
  let component: AppComponent;

  beforeEach(() => {
    return MockBuilder(AppComponent)
      .keep(RouterModule)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({}, {}, '/home')})
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(GoogleAnalyticsService)
      .mock(AppEnvironmentService, {props: signal(mockAppEnvironment)});
  });

  beforeEach(() => {
    fixture = MockRender(AppComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Autism DRIVE'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('Autism DRIVE');
  });
});
