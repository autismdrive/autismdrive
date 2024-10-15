import {AppModule} from '@app/app.module';
import {ApiService} from '@services/api/api.service';
import {mockQuestionnaireInfoList} from '@util/testing/fixtures/mock-questionnaire-info-list';
import {mockExportResponse} from '@util/testing/fixtures/mock-response';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireDataViewComponent} from './questionnaire-data-view.component';
import {of} from 'rxjs';

describe('QuestionnaireDataViewComponent', () => {
  let component: QuestionnaireDataViewComponent;
  let fixture: MockedComponentFixture<QuestionnaireDataViewComponent>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireDataViewComponent, AppModule)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .mock(ApiService, {
        getQuestionnaireInfoList: jest.fn().mockReturnValue(of(mockQuestionnaireInfoList)),
        exportQuestionnaire: jest.fn().mockReturnValue(of(mockExportResponse)),
      });
  });

  beforeEach(() => {
    fixture = MockRender(QuestionnaireDataViewComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
