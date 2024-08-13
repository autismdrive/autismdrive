import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {HelpWrapperComponent} from './help-wrapper.component';

describe('HelpWrapperComponent', () => {
  let component: HelpWrapperComponent;
  let fixture: MockedComponentFixture<HelpWrapperComponent>;

  beforeEach(() => {
    return MockBuilder(HelpWrapperComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(HelpWrapperComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
