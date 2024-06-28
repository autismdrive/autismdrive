import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {SearchFilterComponent} from './search-filter.component';

describe('SearchFilterComponent', () => {
  let component: SearchFilterComponent;
  let fixture: MockedComponentFixture<SearchFilterComponent>;

  beforeEach(() => {
    return MockBuilder(SearchFilterComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchFilterComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
