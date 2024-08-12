import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {faker} from '@faker-js/faker';
import {GeoLocation} from '@models/geolocation';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {SearchService} from '@services/search/search.service';
import {mockResource} from '@util/testing/fixtures/mock-resource';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {SearchComponent} from './search.component';

describe('SearchComponent', () => {
  let component: SearchComponent;
  let fixture: MockedComponentFixture<SearchComponent>;
  const mockGeoLocation = new GeoLocation({
    latitude: faker.location.latitude(),
    longitude: faker.location.longitude(),
    zip_code: faker.location.zipCode(),
    id: 0,
    no_address: true,
  });

  beforeEach(() => {
    return MockBuilder(SearchComponent, AppModule)
      .keep(FormsModule)
      .keep(MaterialModule)
      .keep(ReactiveFormsModule)
      .keep(RouterModule)
      .mock(ApiService, {
        getZipCoords: jest.fn().mockReturnValue(of(mockGeoLocation)),
        getResource: jest.fn().mockReturnValue(of(mockResource)),
        searchStudies: jest.fn().mockReturnValue(of([{hits: []}])),
        getStudy: jest.fn().mockReturnValue(of(mockStudy)),
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      })
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(GoogleAnalyticsService, {})
      .mock(SearchService, {})
      .provide({
        provide: ActivatedRoute,
        useValue: {
          queryParamMap: of({query: '', keys: []}),
        },
      })
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(SearchComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
