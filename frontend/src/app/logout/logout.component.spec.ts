import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {LogoutComponent} from './logout.component';

describe('LogoutComponent', () => {
  let component: LogoutComponent;
  let fixture: MockedComponentFixture<LogoutComponent>;

  beforeEach(() => {
    return MockBuilder(LogoutComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(LogoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
