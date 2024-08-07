import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {StudyFormComponent} from './study-form.component';

describe('StudyFormComponent', () => {
  let component: StudyFormComponent;
  let fixture: MockedComponentFixture<StudyFormComponent>;

  beforeEach(() => {
    return MockBuilder(StudyFormComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(StudyFormComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
