import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {TermsComponent} from './terms.component';
import {ActivatedRoute, RouterModule} from '@angular/router';

describe('TermsComponent', () => {
  let component: TermsComponent;
  let fixture: MockedComponentFixture<TermsComponent>;

  beforeEach(() => {
    return MockBuilder(TermsComponent, AppModule)
      .keep(RouterModule)
      .keep(ActivatedRoute)
      .keep(AuthenticationService)
      .keep(ApiService)
      .keep(GoogleAnalyticsService);
  });

  beforeEach(() => {
    fixture = MockRender(TermsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
