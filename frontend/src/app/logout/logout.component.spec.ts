import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {LogoutComponent} from './logout.component';

describe('LogoutComponent', () => {
  let component: LogoutComponent;
  let fixture: MockedComponentFixture<LogoutComponent>;

  beforeEach(() => {
    return MockBuilder(LogoutComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(NoopAnimationsModule)
      .mock(AuthenticationService, {
        logout: jest.fn().mockReturnValue(of()),
      });
  });

  beforeEach(() => {
    fixture = MockRender(LogoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
