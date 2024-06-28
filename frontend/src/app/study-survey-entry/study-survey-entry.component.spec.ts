import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {StudySurveyEntryComponent} from './study-survey-entry.component';

describe('StudySurveyEntryComponent', () => {
  let component: StudySurveyEntryComponent;
  let fixture: MockedComponentFixture<StudySurveyEntryComponent>;

  beforeEach(() => {
    return MockBuilder(StudySurveyEntryComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(StudySurveyEntryComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
