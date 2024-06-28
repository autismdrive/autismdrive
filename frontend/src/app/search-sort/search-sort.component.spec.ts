import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {SearchSortComponent} from './search-sort.component';

describe('SearchSortComponent', () => {
  let component: SearchSortComponent;
  let fixture: MockedComponentFixture<SearchSortComponent>;

  beforeEach(() => {
    return MockBuilder(SearchSortComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchSortComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
