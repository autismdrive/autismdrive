import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {Participant} from '@models/participant';
import {ApiService} from '@services/api/api.service';
import {mockAdminNote} from '@util/testing/fixtures/mock-admin-note';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {AvatarDialogComponent} from './avatar-dialog.component';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {of} from 'rxjs';
import {mockParticipant} from '@src/util/testing/fixtures/mock-participant';

describe('AvatarDialogComponent', () => {
  let component: AvatarDialogComponent;
  let fixture: MockedComponentFixture<AvatarDialogComponent>;

  beforeEach(() => {
    return MockBuilder(AvatarDialogComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(MaterialModule)
      .mock(ApiService, {
        updateParticipant: jest.fn().mockReturnValue(of(mockParticipant)),
      })
      .provide({
        provide: MatDialogRef,
        useValue: {
          close: (_: any) => {},
          afterOpened: (_: any) => of({}),
        },
      })
      .provide({
        provide: MAT_DIALOG_DATA,
        useValue: {participant: mockParticipant},
      });
  });

  beforeEach(() => {
    fixture = MockRender(AvatarDialogComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
