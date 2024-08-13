import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {LogoComponent} from './logo.component';

describe('LogoComponent', () => {
  let component: LogoComponent;
  let fixture: MockedComponentFixture<LogoComponent>;

  beforeEach(() => {
    return MockBuilder(LogoComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(LogoComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
