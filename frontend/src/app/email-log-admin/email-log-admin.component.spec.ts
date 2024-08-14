import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {EmailLogAdminComponent} from './email-log-admin.component';
import {of} from 'rxjs';

describe('EmailLogAdminComponent', () => {
  let component: EmailLogAdminComponent;
  let fixture: MockedComponentFixture<EmailLogAdminComponent>;

  beforeEach(() => {
    return MockBuilder(EmailLogAdminComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
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
