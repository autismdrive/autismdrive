import {mockCategory} from '@app/shared/fixtures/mock-category';
import {CategoriesService} from '@services/categories/categories.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {SearchTopicsComponent} from './search-topics.component';

describe('SearchTopicsComponent', () => {
  let component: SearchTopicsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(SearchTopicsComponent)
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
