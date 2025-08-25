import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FavoriteTopicsComponent} from './favorite-topics.component';

describe('FavoriteTopicsComponent', () => {
  let component: FavoriteTopicsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getFavoritesByUserAndType: jest.fn().mockReturnValue(of([])),
        addUserFavorites: jest.fn().mockReturnValue(of([])),
      })
      .provide({
        provide: MatDialogRef,
        useValue: {
          close: (_: any) => {},
          afterClosed: jest.fn().mockReturnValue(of({confirm: true})),
        },
      })
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {
          user: mockUser,
          topics: [],
          ages: [],
          languages: [],
          covid19_categories: [],
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(FavoriteTopicsComponent, {currentUser: mockUser}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
