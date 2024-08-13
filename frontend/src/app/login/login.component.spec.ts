import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {LoginComponent} from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: MockedComponentFixture<LoginComponent>;

  beforeEach(() => {
    return MockBuilder(LoginComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(LoginComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
