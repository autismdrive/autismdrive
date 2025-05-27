import {ApiService} from '@services/api/api.service';
import {mockUserFavorite} from '@app/shared/fixtures/mock-user-favorite';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FavoriteResourceButtonComponent} from './favorite-resource-button.component';

describe('FavoriteButtonComponent', () => {
  let component: FavoriteResourceButtonComponent;
  let fixture: MockedComponentFixture<FavoriteResourceButtonComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteResourceButtonComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        addUserFavorites: jest.fn().mockReturnValue(of([mockUserFavorite])),
        deleteUserFavorite: jest.fn().mockReturnValue(of(mockUserFavorite)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteResourceButtonComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
