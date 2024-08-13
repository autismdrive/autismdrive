import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {EmailLogAdminComponent} from './email-log-admin.component';

describe('EmailLogAdminComponent', () => {
  let component: EmailLogAdminComponent;
  let fixture: MockedComponentFixture<EmailLogAdminComponent>;

  beforeEach(() => {
    return MockBuilder(EmailLogAdminComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(EmailLogAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
