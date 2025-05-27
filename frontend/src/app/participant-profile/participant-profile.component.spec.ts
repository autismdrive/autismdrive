import {ApiService} from '@services/api/api.service';
import {mockParticipant} from '@app/shared/fixtures/mock-participant';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ParticipantProfileComponent} from './participant-profile.component';
import {RouterModule} from '@angular/router';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {of} from 'rxjs';

describe('ParticipantProfileComponent', () => {
  let component: ParticipantProfileComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(ParticipantProfileComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {})
      .keep(RouterModule)
      .provide({
        provide: MatDialogRef,
        useValue: {
          close: (_: any) => {},
          afterClosed: jest.fn().mockReturnValue(of({confirm: true})),
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(
      ParticipantProfileComponent,
      {participant: mockParticipant, user: mockUser},
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
