import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {HelpWrapperComponent} from './help-wrapper.component';

describe('HelpWrapperComponent', () => {
  let component: HelpWrapperComponent;
  let fixture: MockedComponentFixture<HelpWrapperComponent>;

  beforeEach(() => {
    return MockBuilder(HelpWrapperComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(HelpWrapperComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
