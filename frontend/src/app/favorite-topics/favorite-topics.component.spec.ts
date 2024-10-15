import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {ApiService} from '@services/api/api.service';
import {mockAdminNote} from '@util/testing/fixtures/mock-admin-note';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FavoriteTopicsComponent} from './favorite-topics.component';
import {of} from 'rxjs';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

describe('FavoriteTopicsComponent', () => {
  let component: FavoriteTopicsComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsComponent, AppModule)
      .keep(MaterialModule)
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
