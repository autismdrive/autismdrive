import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {CategoriesService} from '@services/categories/categories.service';
import {mockCategory} from '@app/shared/fixtures/mock-category';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {SearchBoxComponent} from './search-box.component';

describe('SearchBoxComponent', () => {
  let component: SearchBoxComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(SearchBoxComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(FormsModule)
      .keep(ReactiveFormsModule)
      .keep(RouterModule)
      .provide({
        provide: ActivatedRoute,
        useValue: {
          queryParams: of({query: '', keys: []}),
          queryParamMap: of({query: '', keys: []}),
        },
      })
      .provide({
        provide: CategoriesService,
        useValue: {
          updated: of(true),
          categoriesById: [mockCategory],
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(SearchBoxComponent, {variant: 'light-bg', words: ''}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
