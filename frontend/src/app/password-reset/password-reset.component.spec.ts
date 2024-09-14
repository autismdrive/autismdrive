import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {PasswordResetComponent} from './password-reset.component';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {DeviceDetectorService} from 'ngx-device-detector';
import {of} from 'rxjs';

describe('PasswordResetComponent', () => {
  let component: PasswordResetComponent;
  let fixture: MockedComponentFixture<PasswordResetComponent>;

  beforeEach(() => {
    return MockBuilder(PasswordResetComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {getResourceChangeLog: jest.fn().mockReturnValue(of([]))})
      .keep(ActivatedRoute)
      .keep(RouterModule)
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
