import {signal} from '@angular/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {mockStudyUser} from '@util/testing/fixtures/mock-study-user';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {StudyInquiryComponent} from './study-inquiry.component';

describe('StudyInquiryComponent', () => {
  let component: StudyInquiryComponent;
  let fixture: MockedComponentFixture<StudyInquiryComponent>;

  beforeEach(() => {
    return MockBuilder(StudyInquiryComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(ApiService, {
        getUserStudyInquiries: jest.fn().mockReturnValue(of([mockStudyUser])),
        getUser: jest.fn().mockReturnValue(of(mockUser)),
        sendStudyInquiryEmail: jest.fn().mockReturnValue(of('')),
      })
      .mock(GoogleAnalyticsService, {});
  });

  beforeEach(() => {
    fixture = MockRender(StudyInquiryComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
