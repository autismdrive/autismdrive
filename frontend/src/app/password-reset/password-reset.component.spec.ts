import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';
import {PasswordResetComponent} from './password-reset.component';

describe('PasswordResetComponent', () => {
  let component: PasswordResetComponent;
  let fixture: MockedComponentFixture<PasswordResetComponent>;

  beforeEach(() => {
    return MockBuilder(PasswordResetComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {getResourceChangeLog: jest.fn().mockReturnValue(of([]))})
      .provide({
        provide: ActivatedRoute,
        useValue: makeMockActivatedRoute(
          {},
          {
            role: mockUser.role,
            email_token: 'some-token',
          },
          'reset_password/:role/:email_token',
        ),
      })
      .keep(RouterModule)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(ApiService, {
        getPasswordRequirements: jest.fn().mockReturnValue(
          of({
            regex: '.*',
            instructions: 'some instructions',
          }),
        ),
      })
      .mock(DeviceDetectorService)
      .mock(GoogleAnalyticsService);
  });

  beforeEach(() => {
    fixture = MockRender(PasswordResetComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
