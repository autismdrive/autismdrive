import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {faker} from '@faker-js/faker';
import {AgeRange} from '@models/hit_type';
import {Query} from '@models/query';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SearchFiltersBreadcrumbsComponent} from './search-filters-breadcrumbs.component';

describe('SearchFiltersBreadcrumbsComponent', () => {
  let component: SearchFiltersBreadcrumbsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(SearchFiltersBreadcrumbsComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS).keep(MaterialModule);
  });

  beforeEach(() => {
    const fakeLoc = faker.location.nearbyGPSCoordinate();
    fixture = MockRender(
      SearchFiltersBreadcrumbsComponent,
      {
        query: new Query({
          geo_box: undefined,
          words: '',
          ages: [],
          languages: [],
          sort: {
            field: 'geo_point',
            latitude: fakeLoc[0],
            longitude: fakeLoc[1],
            order: 'asc',
            unit: 'mi',
          },
          start: 0,
          types: ['location', 'resource', 'event'],
        }),
        restrictToMappedResults: false,
        ageLabels: AgeRange.labels,
        languageLabels: {},
        typeLabels: {},
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
