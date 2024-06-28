import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {EmailLogAdminComponent} from './email-log-admin.component';

describe('EmailLogAdminComponent', () => {
  let component: EmailLogAdminComponent;
  let fixture: MockedComponentFixture<EmailLogAdminComponent>;

  beforeEach(() => {
    return MockBuilder(EmailLogAdminComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(EmailLogAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
