import {signal} from '@angular/core';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {FormlyConfig} from '@app/app.config';
import {FormlyMatInputModule} from '@ngx-formly/material/input';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {LoginComponent} from './login.component';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {DeviceDetectorService} from 'ngx-device-detector';
import {AuthenticationService} from '@app/_services/authentication/authentication-service';
import {of} from 'rxjs';
import {FormlyModule} from '@ngx-formly/core';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: MockedComponentFixture<any>;
  let windowSpy: jest.SpyInstance;

  beforeEach(() => {
    return MockBuilder(LoginComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(FormlyMatInputModule)
      .keep(RouterModule)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({returnUrl: 'http://some.url'},{email_token: 'some_token'},'login')})
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(DeviceDetectorService)
      .mock(GoogleAnalyticsService)
  });

  beforeEach(() => {
    windowSpy = jest.spyOn(globalThis, "window", "get");
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
