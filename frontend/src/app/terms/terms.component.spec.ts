import {signal} from '@angular/core';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockParticipant} from '@app/shared/fixtures/mock-participant';
import {mockIdentificationQuestionnaire} from '@app/shared/fixtures/mock-questionnaire';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
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
        addParticipant: jest.fn().mockReturnValue(of(mockParticipant)),
      })
      .keep(PdfJsViewerModule)
      .mock(GoogleAnalyticsService, {});
  });

  beforeEach(() => {
    fixture = MockRender(TermsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
