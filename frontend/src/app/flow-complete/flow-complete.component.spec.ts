import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FlowCompleteComponent} from './flow-complete.component';

describe('FlowCompleteComponent', () => {
  let component: FlowCompleteComponent;
  let fixture: MockedComponentFixture<FlowCompleteComponent>;

  beforeEach(() => {
    return MockBuilder(FlowCompleteComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FlowCompleteComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
