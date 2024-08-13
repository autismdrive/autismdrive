import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {ResizeTextareaComponent} from './resize-textarea.component';

describe('ResizeTextareaComponent', () => {
  let component: ResizeTextareaComponent;
  let fixture: MockedComponentFixture<ResizeTextareaComponent>;

  beforeEach(() => {
    return MockBuilder(ResizeTextareaComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(ResizeTextareaComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
