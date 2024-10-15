import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
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
  let fixture: MockedComponentFixture<LoginComponent>;

  beforeEach(() => {
    return MockBuilder(LoginComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .keep(MaterialModule)
      .keep(FormlyModule)
      .mock(DeviceDetectorService)
      .mock(GoogleAnalyticsService)
      .keep(ActivatedRoute)
      .keep(RouterModule);
  });

  beforeEach(() => {
    fixture = MockRender(LoginComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
