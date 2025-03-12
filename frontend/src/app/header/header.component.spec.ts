import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {mockUser} from '@util/testing/fixtures/mock-user';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {HeaderComponent} from './header.component';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: MockedComponentFixture<HeaderComponent>;

  beforeEach(() => {
    return MockBuilder(HeaderComponent)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {currentUser: of(mockUser)})
      .mock(ApiService, {});
  });

  beforeEach(() => {
    fixture = MockRender(HeaderComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
