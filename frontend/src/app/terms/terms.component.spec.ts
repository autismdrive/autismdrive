import {signal} from '@angular/core';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {makeMockActivatedRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockParticipant} from '@util/testing/fixtures/mock-participant';
import {mockIdentificationQuestionnaire} from '@util/testing/fixtures/mock-questionnaire';
import {mockQuestionnaireMeta} from '@util/testing/fixtures/mock-questionnaire-meta';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {of} from 'rxjs';
import {TermsComponent} from './terms.component';

describe('TermsComponent', () => {
  let component: TermsComponent;
  let fixture: MockedComponentFixture<TermsComponent>;

  beforeEach(() => {
    return MockBuilder(TermsComponent)
      .keep(RouterModule)
      .provide({
        provide: ActivatedRoute,
        useValue: makeMockActivatedRoute(
          {},
          {
            relationship: mockIdentificationQuestionnaire.relationship_to_participant,
            preview: true,
          },
          'terms/:relationship',
        ),
      })
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(ApiService, {
        addParticipant: jest.fn().mockReturnValue(of(mockParticipant))
      })
      .keep(PdfJsViewerModule)
      .keep(GoogleAnalyticsService);
  });

  beforeEach(() => {
    fixture = MockRender(TermsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
