import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {LogoComponent} from './logo.component';

describe('LogoComponent', () => {
  let component: LogoComponent;
  let fixture: MockedComponentFixture<LogoComponent>;

  beforeEach(() => {
    return MockBuilder(LogoComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(LogoComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
