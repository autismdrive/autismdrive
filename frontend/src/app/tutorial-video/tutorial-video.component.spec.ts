import {LOCAL_STORAGE} from '@app/tokens';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {TutorialVideoComponent} from './tutorial-video.component';

describe('TutorialVideoComponent', () => {
  let component: TutorialVideoComponent;
  let fixture: MockedComponentFixture<TutorialVideoComponent>;

  beforeEach(() => {
    return MockBuilder(TutorialVideoComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide({provide: LOCAL_STORAGE, useValue: globalThis.localStorage});
  });

  beforeEach(() => {
    fixture = MockRender(TutorialVideoComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
