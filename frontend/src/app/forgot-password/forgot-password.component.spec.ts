import {RouterModule} from '@angular/router';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {ForgotPasswordComponent} from './forgot-password.component';

describe('ForgotPasswordComponent', () => {
  let component: ForgotPasswordComponent;
  let fixture: MockedComponentFixture<ForgotPasswordComponent>;

  beforeEach(() => {
    return MockBuilder(ForgotPasswordComponent)
      .keep(RouterModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        sendResetPasswordEmail: jest.fn().mockReturnValue(of('')),
      });
  });

  beforeEach(() => {
    fixture = MockRender(ForgotPasswordComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
