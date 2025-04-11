import {TestBed} from '@angular/core/testing';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {AuthenticationStateService} from '@services/authentication/authentication-state-service';
import {MockProvider} from 'ng-mocks';
import {GoogleAnalyticsService} from './google-analytics.service';

describe('GoogleAnalyticsService', () => {
  beforeEach(() =>
    TestBed.configureTestingModule({
      providers: [MockProvider(AppEnvironmentService), MockProvider(AuthenticationStateService)],
    }),
  );

  it('should be created', () => {
    const service: GoogleAnalyticsService = TestBed.get(GoogleAnalyticsService);
    expect(service).toBeTruthy();
  });
});
