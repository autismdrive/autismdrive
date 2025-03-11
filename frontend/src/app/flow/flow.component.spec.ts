import {ActivatedRoute} from '@angular/router';
import {FormlyConfig} from '@app/app.config';
import {FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {makeMockActivatedRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockFlow} from '@util/testing/fixtures/mock-flow';
import {mockParticipant} from '@util/testing/fixtures/mock-participant';
import {mockIdentificationQuestionnaire} from '@util/testing/fixtures/mock-questionnaire';
import {mockQuestionnaireMeta} from '@util/testing/fixtures/mock-questionnaire-meta';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {FlowComponent} from './flow.component';

describe('EnrollmentFlowComponent', () => {
  let component: FlowComponent;
  let fixture: MockedComponentFixture<FlowComponent>;

  beforeEach(() => {
    return MockBuilder(FlowComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
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
      .mock(AuthenticationService, {currentUser: of(mockUser)})
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
