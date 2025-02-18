import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FlowComponent} from './flow.component';

describe('EnrollmentFlowComponent', () => {
  let component: FlowComponent;
  let fixture: MockedComponentFixture<FlowComponent>;

  beforeEach(() => {
    return MockBuilder(FlowComponent).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FlowComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
