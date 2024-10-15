import {AppModule} from '@app/app.module';
import {sortMethods} from '@models/sort_method';
import createClone from 'rfdc';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SearchSortComponent} from './search-sort.component';

describe('SearchSortComponent', () => {
  let component: SearchSortComponent;
  let fixture: MockedComponentFixture<any>;
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
