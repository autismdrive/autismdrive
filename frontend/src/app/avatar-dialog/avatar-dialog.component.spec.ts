import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ApiService} from '@services/api/api.service';
import {mockParticipant} from '@util/testing/fixtures/mock-participant';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {AvatarDialogComponent} from './avatar-dialog.component';

describe('AvatarDialogComponent', () => {
  let component: AvatarDialogComponent;
  let fixture: MockedComponentFixture<AvatarDialogComponent>;

  beforeEach(() => {
    return MockBuilder(AvatarDialogComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
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
