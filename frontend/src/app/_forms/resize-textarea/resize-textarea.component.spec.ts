import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {ResizeTextareaComponent} from './resize-textarea.component';

describe('ResizeTextareaComponent', () => {
  let component: ResizeTextareaComponent;
  let fixture: MockedComponentFixture<ResizeTextareaComponent>;

  beforeEach(() => {
    return MockBuilder(ResizeTextareaComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(ResizeTextareaComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
