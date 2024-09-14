import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {MaterialModule} from '@app/material/material.module';
import {FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog.component';
import {BrowserAnimationsModule, NoopAnimationsModule} from '@angular/platform-browser/animations';

describe('FavoriteTopicsDialogComponent', () => {
  let component: FavoriteTopicsDialogComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsDialogComponent)
      .keep(FormlyModule)
      .keep(FormsModule)
      .keep(MaterialModule)
      .keep(ReactiveFormsModule)
      .keep(NoopAnimationsModule)
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
    fixture = MockRender(
      FavoriteTopicsDialogComponent,
      {animations: {'@transitionMessages': {}}},
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
