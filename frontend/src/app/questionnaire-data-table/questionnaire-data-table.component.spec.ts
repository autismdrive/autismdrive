import {mockQuestionnaireMeta} from '@app/shared/fixtures/mock-questionnaire-meta';
import {mockExportResponse} from '@app/shared/fixtures/mock-response';
import {ApiService} from '@services/api/api.service';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';
import {QuestionnaireDataTableComponent} from './questionnaire-data-table.component';

describe('QuestionnaireDataTableComponent', () => {
  let component: QuestionnaireDataTableComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireDataTableComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getQuestionnaireList: jest.fn().mockReturnValue(of([])),
        getQuestionnaireListMeta: jest.fn().mockReturnValue(of(mockQuestionnaireMeta)),
        exportQuestionnaire: jest.fn().mockReturnValue(of(mockExportResponse)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(
      QuestionnaireDataTableComponent,
      {
        questionnaire_info: {table_name: 'test_table'},
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
