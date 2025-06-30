import {RouterModule} from '@angular/router';
import {mockUser} from '@app/shared/fixtures/mock-user';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {UserAdminComponent} from './user-admin.component';

describe('UserAdminComponent', () => {
  let component: UserAdminComponent;
  let fixture: MockedComponentFixture<UserAdminComponent>;

  beforeEach(() => {
    return MockBuilder(UserAdminComponent)
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
