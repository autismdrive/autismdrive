import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {mockFlowCompleteRoute} from '@util/testing/fixtures/mock-activated-route';
import {mockFlow} from '@util/testing/fixtures/mock-flow';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FlowCompleteComponent} from './flow-complete.component';

describe('FlowCompleteComponent', () => {
  let component: FlowCompleteComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(FlowCompleteComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(RouterModule.forRoot([{path: '/search', component: FlowCompleteComponent}]), {
        dependency: false,
      })
      .provide({provide: ActivatedRoute, useValue: mockFlowCompleteRoute});
  });

  beforeEach(() => {
    fixture = MockRender(FlowCompleteComponent, {flow: mockFlow}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
