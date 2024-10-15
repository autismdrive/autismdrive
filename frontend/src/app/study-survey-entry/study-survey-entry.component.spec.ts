import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {StudySurveyEntryComponent} from './study-survey-entry.component';

describe('StudySurveyEntryComponent', () => {
  let component: StudySurveyEntryComponent;
  let fixture: MockedComponentFixture<StudySurveyEntryComponent>;

  beforeEach(() => {
    return MockBuilder(StudySurveyEntryComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(StudySurveyEntryComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
