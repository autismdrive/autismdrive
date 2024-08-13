import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {FlowIntroComponent} from './flow-intro.component';

describe('FlowIntroComponent', () => {
  let component: FlowIntroComponent;
  let fixture: MockedComponentFixture<FlowIntroComponent>;

  beforeEach(() => {
    return MockBuilder(FlowIntroComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(FlowIntroComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
