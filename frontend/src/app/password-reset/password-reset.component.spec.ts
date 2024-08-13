import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {PasswordResetComponent} from './password-reset.component';

describe('PasswordResetComponent', () => {
  let component: PasswordResetComponent;
  let fixture: MockedComponentFixture<PasswordResetComponent>;

  beforeEach(() => {
    return MockBuilder(PasswordResetComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(PasswordResetComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
