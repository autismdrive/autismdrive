import {signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockFlow} from '@app/shared/fixtures/mock-flow';
import {mockParticipant} from '@app/shared/fixtures/mock-participant';
import {mockIdentificationQuestionnaire} from '@app/shared/fixtures/mock-questionnaire';
import {mockQuestionnaireMeta} from '@app/shared/fixtures/mock-questionnaire-meta';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FlowComponent} from './flow.component';

describe('EnrollmentFlowComponent', () => {
  let component: FlowComponent;
  let fixture: MockedComponentFixture<FlowComponent>;

  beforeEach(() => {
    return MockBuilder(FlowComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .provide({
        provide: ActivatedRoute,
        useValue: of(
          makeMockActivatedRoute(
            {},
            {
              flowName: mockIdentificationQuestionnaire.__tablename__,
              participantId: mockUser.id,
            },
            'flow/:flowName/:participantId',
          ),
        ),
      })
      .mock(GoogleAnalyticsService)
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(ApiService, {
        getFlow: jest.fn().mockReturnValue(of(mockFlow)),
        getParticipant: jest.fn().mockReturnValue(of(mockParticipant)),
        getQuestionnaireMeta: jest.fn().mockReturnValue(of(mockQuestionnaireMeta)),
        getQuestionnaire: jest.fn().mockReturnValue(of(mockIdentificationQuestionnaire)),
        submitQuestionnaire: jest.fn().mockReturnValue(of(mockIdentificationQuestionnaire)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(FlowComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
