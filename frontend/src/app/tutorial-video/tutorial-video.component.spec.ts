import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {TutorialVideoComponent} from './tutorial-video.component';

describe('TutorialVideoComponent', () => {
  let component: TutorialVideoComponent;
  let fixture: MockedComponentFixture<TutorialVideoComponent>;

  beforeEach(() => {
    return MockBuilder(TutorialVideoComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(TutorialVideoComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
