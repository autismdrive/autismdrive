import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from 'ng-mocks';
import {QuestionnaireStepComponent} from './questionnaire-step.component';

describe('QuestionnaireStepComponent', () => {
  let component: QuestionnaireStepComponent;
  let fixture: MockedComponentFixture<QuestionnaireStepComponent>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireStepComponent, AppModule);
  });

  beforeEach(() => {
    fixture = MockRender(QuestionnaireStepComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
