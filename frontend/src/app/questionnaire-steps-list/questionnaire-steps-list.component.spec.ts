import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireStepsListComponent} from './questionnaire-steps-list.component';

describe('QuestionnaireStepsListComponent', () => {
  let component: QuestionnaireStepsListComponent;
  let fixture: MockedComponentFixture<QuestionnaireStepsListComponent>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireStepsListComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(QuestionnaireStepsListComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
