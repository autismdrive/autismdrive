import {signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {mockUserDetailsRoute} from '@app/shared/fixtures/mock-activated-route';
import {makeMockEmailLog} from '@app/shared/fixtures/mock-email-log';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {UserAdminDetailsComponent} from './user-admin-details.component';

describe('UserAdminDetailsComponent', () => {
  let component: UserAdminDetailsComponent;
  let fixture: MockedComponentFixture<UserAdminDetailsComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminDetailsComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getUser: jest.fn().mockReturnValue(of(mockUser)),
        getUserEmailLog: jest.fn().mockReturnValue(of(makeMockEmailLog({user_id: mockUser.id}))),
        getUserAdminNotes: jest.fn().mockReturnValue(of()),
        getUserResourceChangeLog: jest.fn().mockReturnValue(of()),
        getParticipantStepLog: jest.fn().mockReturnValue(of()),
        exportUserQuestionnaire: jest.fn().mockReturnValue(of()),
        updateUser: jest.fn().mockReturnValue(of()),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .provide({provide: ActivatedRoute, useValue: mockUserDetailsRoute});
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminDetailsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
