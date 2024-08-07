import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {SearchFiltersBreadcrumbsComponent} from './search-filters-breadcrumbs.component';

describe('SearchFiltersBreadcrumbsComponent', () => {
  let component: SearchFiltersBreadcrumbsComponent;
  let fixture: MockedComponentFixture<SearchFiltersBreadcrumbsComponent>;

  beforeEach(() => {
    return MockBuilder(SearchFiltersBreadcrumbsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(SearchFiltersBreadcrumbsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
