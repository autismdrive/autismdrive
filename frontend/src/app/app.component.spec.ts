import {TestBed} from '@angular/core/testing';
import {ActivatedRoute, Router, RouterModule} from '@angular/router';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {of} from 'rxjs';
import {AppComponent} from './app.component';

describe('AppComponent', () => {
  let fixture: MockedComponentFixture<AppComponent>;
  let component: AppComponent;

  beforeEach(() => {
    return MockBuilder(AppComponent)
      .keep(RouterModule)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({},{},'/home')})
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(GoogleAnalyticsService);
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
