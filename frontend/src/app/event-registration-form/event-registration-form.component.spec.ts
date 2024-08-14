import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {MaterialModule} from '@app/material/material.module';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {EventRegistrationFormComponent} from './event-registration-form.component';

describe('EventRegistrationFormComponent', () => {
  let component: EventRegistrationFormComponent;
  let fixture: MockedComponentFixture<EventRegistrationFormComponent>;

  beforeEach(() => {
    return (
      MockBuilder(EventRegistrationFormComponent, AppModule)
        .keep(MaterialModule)
        .keep(NG_MOCKS_ROOT_PROVIDERS)
        .keep(RouterModule.forRoot([{path: '', component: EventRegistrationFormComponent}]))
        .mock(ApiService, {
          addUser: jest.fn().mockReturnValue(of(mockUser)),
          submitRegistration: jest.fn().mockReturnValue(of()),
          submitQuestionnaire: jest.fn().mockReturnValue(of()),
        })
        // .provide({provide: ActivatedRoute, useValue: mockActivatedRouteWithEventId})
        .mock(GoogleAnalyticsService)
        .mock(AuthenticationService, {currentUser: of(mockUser)})
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
