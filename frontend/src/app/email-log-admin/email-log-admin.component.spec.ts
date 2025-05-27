import {signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {makeMockActivatedRoute} from '@app/shared/fixtures/mock-activated-route';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {EmailLogAdminComponent} from './email-log-admin.component';
import {of} from 'rxjs';

describe('EmailLogAdminComponent', () => {
  let component: EmailLogAdminComponent;
  let fixture: MockedComponentFixture<EmailLogAdminComponent>;

  beforeEach(() => {
    return MockBuilder(EmailLogAdminComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({provide: ActivatedRoute, useValue: makeMockActivatedRoute({}, {}, '/email-log')})
      .mock(AuthenticationService, {currentUser: signal(mockUser)})
      .mock(ApiService, {getAllEmailLog: jest.fn().mockReturnValue(of([]))});
  });

  beforeEach(() => {
    fixture = MockRender(EmailLogAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
