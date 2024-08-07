import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {ForgotPasswordComponent} from './forgot-password.component';

describe('ForgotPasswordComponent', () => {
  let component: ForgotPasswordComponent;
  let fixture: MockedComponentFixture<ForgotPasswordComponent>;

  beforeEach(() => {
    return MockBuilder(ForgotPasswordComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ForgotPasswordComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
