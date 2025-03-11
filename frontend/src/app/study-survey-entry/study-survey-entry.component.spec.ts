import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {StudySurveyEntryComponent} from './study-survey-entry.component';

describe('StudySurveyEntryComponent', () => {
  let component: StudySurveyEntryComponent;
  let fixture: MockedComponentFixture<StudySurveyEntryComponent>;

  beforeEach(() => {
    return MockBuilder(StudySurveyEntryComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(ApiService, {
        getUser: jest.fn().mockReturnValue(of(mockUser)),
        sendStudyInquiryEmail: jest.fn().mockReturnValue(of("")),
      });
  });

  beforeEach(() => {
    fixture = MockRender(StudySurveyEntryComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
