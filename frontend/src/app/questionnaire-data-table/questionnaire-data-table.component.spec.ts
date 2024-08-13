import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireDataTableComponent} from './questionnaire-data-table.component';

describe('QuestionnaireDataTableComponent', () => {
  let component: QuestionnaireDataTableComponent;
  let fixture: MockedComponentFixture<QuestionnaireDataTableComponent>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireDataTableComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(QuestionnaireDataTableComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
