import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {CategoriesService} from '@services/categories/categories.service';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {SearchTopicsComponent} from './search-topics.component';
import {of} from 'rxjs';

describe('SearchTopicsComponent', () => {
  let component: SearchTopicsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(SearchTopicsComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({
        provide: CategoriesService,
        useValue: {
          updated: of(true),
          categoriesById: [mockCategory],
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(SearchTopicsComponent, {category: mockCategory}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
