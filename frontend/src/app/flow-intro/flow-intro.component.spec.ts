import {AppModule} from '@app/app.module';
import {mockFlow} from '@util/testing/fixtures/mock-flow';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FlowIntroComponent} from './flow-intro.component';

describe('FlowIntroComponent', () => {
  let component: FlowIntroComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FlowIntroComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FlowIntroComponent, {flow: mockFlow}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
