import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {FlowCompleteComponent} from './flow-complete.component';

describe('FlowCompleteComponent', () => {
  let component: FlowCompleteComponent;
  let fixture: MockedComponentFixture<FlowCompleteComponent>;

  beforeEach(() => {
    return MockBuilder(FlowCompleteComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(FlowCompleteComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
