import {signal} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RouterModule} from '@angular/router';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {mockParticipant} from '@util/testing/fixtures/mock-participant';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {EventRegistrationFormComponent} from './event-registration-form.component';

describe('EventRegistrationFormComponent', () => {
  let component: EventRegistrationFormComponent;
  let fixture: MockedComponentFixture<EventRegistrationFormComponent>;

  mockParticipant.user_id = mockUser.id;
  const mockUserWithSelfParticipant = new User({...mockUser, participants: [mockParticipant]});

  beforeEach(() => {
    return (
      MockBuilder(EventRegistrationFormComponent)
        .keep(NG_MOCKS_ROOT_PROVIDERS)
        .keep(RouterModule.forRoot([{path: '', component: EventRegistrationFormComponent}]))
        .mock(ApiService, {
          addUser: jest.fn().mockReturnValue(of(mockUser)),
          submitRegistration: jest.fn().mockReturnValue(of()),
          submitQuestionnaire: jest.fn().mockReturnValue(of()),
        })
        // .provide({provide: ActivatedRoute, useValue: mockActivatedRouteWithEventId})
        .mock(GoogleAnalyticsService)
        .mock(AuthenticationService, {currentUser: signal(mockUserWithSelfParticipant)})
        .provide({provide: MatDialogRef, useValue: {close: (_: any) => {}}})
        .provide({
          provide: MAT_DIALOG_DATA,
          useValue: {
            title: 'some title',
            event_id: 0,
          },
        })
    );
  });

  beforeEach(() => {
    fixture = MockRender(EventRegistrationFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
