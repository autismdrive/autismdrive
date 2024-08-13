import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {LogoutComponent} from './logout.component';

describe('LogoutComponent', () => {
  let component: LogoutComponent;
  let fixture: MockedComponentFixture<LogoutComponent>;

  beforeEach(() => {
    return MockBuilder(LogoutComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(LogoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
