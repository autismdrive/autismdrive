import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {AuthenticationStateService} from '@services/authentication/authentication-state-service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {TimedOutComponent} from './timed-out.component';

describe('TimedOutComponent', () => {
  let component: TimedOutComponent;
  let fixture: MockedComponentFixture<TimedOutComponent>;

  beforeEach(() => {
    return MockBuilder(TimedOutComponent)
      .keep(NoopAnimationsModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(AuthenticationService, {
        logout: jest.fn().mockImplementation(() => {
          localStorage.removeItem(AuthenticationStateService.LOCAL_TOKEN_KEY);
        }),
      });
  });

  beforeEach(() => {
    fixture = MockRender(TimedOutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
