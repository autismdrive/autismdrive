import {signal} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {GoogleMapsModule} from '@angular/google-maps';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {mockResource} from '@app/shared/fixtures/mock-resource';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {LOCAL_STORAGE} from '@app/tokens';
import {faker} from '@faker-js/faker';
import {GeoLocation} from '@models/geolocation';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {SearchService} from '@services/search/search.service';
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
    return MockBuilder(SearchComponent)
      .keep(GoogleMapsModule)
      .keep(ReactiveFormsModule)
      .keep(RouterModule)
      .mock(ApiService, {
        getZipCoords: jest.fn().mockReturnValue(of(mockGeoLocation)),
        getResource: jest.fn().mockReturnValue(of(mockResource)),
        searchStudies: jest.fn().mockReturnValue(of([{hits: []}])),
        getStudy: jest.fn().mockReturnValue(of(mockStudy)),
        getStudiesByStatus: jest.fn().mockReturnValue(of([mockStudy])),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(GoogleAnalyticsService, {})
      .mock(GoogleMapsLibraryService, {core: signal(undefined)})
      .mock(SearchService, {})
      .provide({provide: LOCAL_STORAGE, useValue: globalThis.localStorage})
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
