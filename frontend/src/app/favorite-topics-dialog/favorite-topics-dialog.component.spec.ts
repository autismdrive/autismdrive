import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {ApiService} from '@services/api/api.service';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog.component';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {of} from 'rxjs';

describe('FavoriteTopicsDialogComponent', () => {
  let component: FavoriteTopicsDialogComponent;
  let fixture: MockedComponentFixture<FavoriteTopicsDialogComponent>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsDialogComponent, AppModule)
      .keep(MaterialModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([mockCategory])),
      })

      .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
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
    fixture = MockRender(FavoriteTopicsDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
