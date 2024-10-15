import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {TimedoutComponent} from './timed-out.component';

describe('TimedoutComponent', () => {
  let component: TimedoutComponent;
  let fixture: MockedComponentFixture<TimedoutComponent>;

  beforeEach(() => {
    return MockBuilder(TimedoutComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(TimedoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
