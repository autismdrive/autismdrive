import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {PasswordResetComponent} from './password-reset.component';

describe('PasswordResetComponent', () => {
  let component: PasswordResetComponent;
  let fixture: MockedComponentFixture<PasswordResetComponent>;

  beforeEach(() => {
    return MockBuilder(PasswordResetComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(PasswordResetComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
