import {ReactiveFormsModule} from '@angular/forms';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {ApiService} from '@services/api/api.service';
import {mockCategory} from '@app/shared/fixtures/mock-category';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog.component';

describe('FavoriteTopicsDialogComponent', () => {
  let component: FavoriteTopicsDialogComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FavoriteTopicsDialogComponent)
      .keep(ReactiveFormsModule)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getCategoryTree: jest.fn().mockReturnValue(of([mockCategory])),
      })
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
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
