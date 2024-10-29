import {AppModule} from '@app/app.module';
import {SortMethod, sortMethods} from '@models/sort_method';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import createClone from 'rfdc';
import {SearchSortComponent} from './search-sort.component';

interface SearchSortParams {
  selectedSort: SortMethod;
  sortMethods: Record<string, SortMethod>;
}

describe('SearchSortComponent', () => {
  let component: SearchSortComponent;
  let fixture: MockedComponentFixture<SearchSortComponent, SearchSortParams>;
  const mockSortMethods = createClone()(sortMethods);
  const mockLocation = {latitude: 0, longitude: 0};
  mockSortMethods.DISTANCE.sortQuery.latitude = mockLocation.latitude;
  mockSortMethods.DISTANCE.sortQuery.longitude = mockLocation.longitude;

  beforeEach(() => {
    return MockBuilder(SearchSortComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(
      SearchSortComponent,
      {
        selectedSort: mockSortMethods.DISTANCE,
        sortMethods: mockSortMethods,
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
