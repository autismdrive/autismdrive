import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {mockQuestionnaireListMeta} from '@util/testing/fixtures/mock-questionnaire-list-meta';
import {mockExportResponse} from '@util/testing/fixtures/mock-response';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireDataTableComponent} from './questionnaire-data-table.component';
import {of} from 'rxjs';

describe('QuestionnaireDataTableComponent', () => {
  let component: QuestionnaireDataTableComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireDataTableComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getQuestionnaireList: jest.fn().mockReturnValue(of([])),
        getQuestionnaireListMeta: jest.fn().mockReturnValue(of(mockQuestionnaireListMeta)),
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
