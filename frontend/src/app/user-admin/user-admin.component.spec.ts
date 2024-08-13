import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {UserAdminComponent} from './user-admin.component';

describe('UserAdminComponent', () => {
  let component: UserAdminComponent;
  let fixture: MockedComponentFixture<UserAdminComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
