import {signal} from '@angular/core';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
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

  beforeEach(() => {
    return MockBuilder(LoginComponent)
      .keep(FormlyMatInputModule)
      .keep(RouterModule)
      .keep(NoopAnimationsModule)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .provide({
        provide: ActivatedRoute,
        useValue: makeMockActivatedRoute({returnUrl: 'http://some.url'}, {email_token: 'some_token'}, 'login'),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(DeviceDetectorService)
      .mock(GoogleAnalyticsService);
  });

  beforeEach(() => {
    fixture = MockRender(LoginComponent, {animations: {'@transitionMessages': {}}}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
