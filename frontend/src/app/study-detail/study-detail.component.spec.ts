import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {StudyDetailComponent} from './study-detail.component';

describe('StudyDetailComponent', () => {
  let component: StudyDetailComponent;
  let fixture: MockedComponentFixture<StudyDetailComponent>;

  beforeEach(() => {
    return MockBuilder(StudyDetailComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(StudyDetailComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
