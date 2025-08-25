import {signal} from '@angular/core';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {customFormlyConfig} from '@app/app.config';
import {mockProfileRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockFlow} from '@app/shared/fixtures/mock-flow';
import {mockStudy} from '@app/shared/fixtures/mock-study';
import {mockStudyUser} from '@app/shared/fixtures/mock-study-user';
import {mockUser, mockUserMeta} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@app/shared/services/api/api.service';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {ProfileComponent} from './profile.component';

describe('ProfileComponent', () => {
  let component: ProfileComponent;
  let fixture: MockedComponentFixture<ProfileComponent>;

  beforeEach(() => {
    // @ts-ignore
    return MockBuilder(ProfileComponent)
      .keep(RouterModule)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]))
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
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
