import {AppModule} from '@app/app.module';
import {mockFlow} from '@util/testing/fixtures/mock-flow';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireStepsListComponent} from './questionnaire-steps-list.component';

describe('QuestionnaireStepsListComponent', () => {
  let component: QuestionnaireStepsListComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireStepsListComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(
      QuestionnaireStepsListComponent,
      {
        flow: mockFlow,
        stepIndex: 0,
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
