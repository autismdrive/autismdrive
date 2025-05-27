import {signal} from '@angular/core';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMatInputModule} from '@ngx-formly/material/input';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {LoginComponent} from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: MockedComponentFixture<any>;
  let windowSpy: jest.SpyInstance;

  beforeEach(() => {
    return MockBuilder(LoginComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(FormlyMatInputModule)
      .keep(RouterModule)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({
        provide: ActivatedRoute,
        useValue: makeMockActivatedRoute({returnUrl: 'http://some.url'}, {email_token: 'some_token'}, 'login'),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(DeviceDetectorService)
      .mock(GoogleAnalyticsService);
  });

  beforeEach(() => {
    windowSpy = jest.spyOn(globalThis, 'window', 'get');
    windowSpy.mockImplementation(() => ({
      scroll: jest.fn(),
    }));

    fixture = MockRender(LoginComponent, {animations: {'@transitionMessages': {}}}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  afterEach(() => {
    windowSpy.mockRestore();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
