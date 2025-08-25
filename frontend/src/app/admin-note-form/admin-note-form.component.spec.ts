import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {mockAdminNote} from '@app/shared/fixtures/mock-admin-note';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {AdminNoteFormComponent} from './admin-note-form.component';

describe('AdminNoteFormComponent', () => {
  let component: AdminNoteFormComponent;
  let fixture: MockedComponentFixture<AdminNoteFormComponent>;

  beforeEach(() => {
    return MockBuilder(AdminNoteFormComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({
        provide: MatDialogRef,
        useValue: {
          close: (_: any) => {},
        },
      })
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {adminNote: mockAdminNote},
      });
  });

  beforeEach(() => {
    fixture = MockRender(AdminNoteFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
