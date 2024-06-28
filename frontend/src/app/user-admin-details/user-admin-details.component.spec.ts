import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {UserAdminDetailsComponent} from './user-admin-details.component';

describe('UserAdminDetailsComponent', () => {
  let component: UserAdminDetailsComponent;
  let fixture: MockedComponentFixture<UserAdminDetailsComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminDetailsComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminDetailsComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
