import {ActivatedRoute, RouterModule} from '@angular/router';
import {ApiService} from '@app/_services/api/api.service';
import {AuthenticationService} from '@app/_services/authentication/authentication-service';
import {AppModule} from '@app/app.module';
import {mockStudyUser} from '@src/util/testing/fixtures/mock-study-user';
import {mockProfileRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockFlow} from '@util/testing/fixtures/mock-flow';
import {mockStudy} from '@util/testing/fixtures/mock-study';
import {mockUser, mockUserMeta} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {ProfileComponent} from './profile.component';

describe('ProfileComponent', () => {
  let component: ProfileComponent;
  let fixture: MockedComponentFixture<ProfileComponent>;

  beforeEach(() => {
    // @ts-ignore
    return MockBuilder(ProfileComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(ApiService, {
        getUserMeta: jest.fn().mockReturnValue(of(mockUserMeta)),
        getUserStudyInquiries: jest.fn().mockReturnValue(of([mockStudyUser])),
        getStudies: jest.fn().mockReturnValue(of([mockStudy])),
        getUser: jest.fn().mockReturnValue(of(mockUser)),
        getFlow: jest.fn().mockReturnValue(of(mockFlow)),
        addUserMeta: jest.fn().mockReturnValue(of(mockUserMeta)),
      })
      .provide({provide: ActivatedRoute, useValue: mockProfileRoute});
  });

  beforeEach(() => {
    fixture = MockRender(ProfileComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
