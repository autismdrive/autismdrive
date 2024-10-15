import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {UserAdminComponent} from './user-admin.component';
import {RouterModule} from '@angular/router';
import {of} from 'rxjs';

describe('UserAdminComponent', () => {
  let component: UserAdminComponent;
  let fixture: MockedComponentFixture<UserAdminComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule)
      .mock(ApiService, {findUsers: jest.fn().mockReturnValue(of({pages: 1, total: 1, users: [mockUser]}))});
  });

  beforeEach(() => {
    fixture = MockRender(UserAdminComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
