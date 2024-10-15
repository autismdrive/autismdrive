import {AppModule} from '@app/app.module';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockActivatedRouteWithUserId} from '@util/testing/fixtures/mock-activated-route';
import {makeMockEmailLog, mockEmailLog} from '@util/testing/fixtures/mock-email-log';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {UserAdminDetailsComponent} from './user-admin-details.component';
import {of} from 'rxjs';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '@app/_services/api/api.service';

describe('UserAdminDetailsComponent', () => {
  let component: UserAdminDetailsComponent;
  let fixture: MockedComponentFixture<UserAdminDetailsComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminDetailsComponent, AppModule)
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
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .provide({provide: ActivatedRoute, useValue: mockActivatedRouteWithUserId});
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminDetailsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
