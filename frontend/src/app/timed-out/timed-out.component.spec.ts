import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {TimedoutComponent} from './timed-out.component';

describe('TimedoutComponent', () => {
  let component: TimedoutComponent;
  let fixture: MockedComponentFixture<TimedoutComponent>;

  beforeEach(() => {
    return MockBuilder(TimedoutComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(TimedoutComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
