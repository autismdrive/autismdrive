import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {UserAdminComponent} from './user-admin.component';

describe('UserAdminComponent', () => {
  let component: UserAdminComponent;
  let fixture: MockedComponentFixture<UserAdminComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
