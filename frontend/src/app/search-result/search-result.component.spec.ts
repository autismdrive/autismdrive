import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {SearchResultComponent} from './search-result.component';

describe('SearchResultComponent', () => {
  let component: SearchResultComponent;
  let fixture: MockedComponentFixture<SearchResultComponent>;

  beforeEach(() => {
    return MockBuilder(SearchResultComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchResultComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
