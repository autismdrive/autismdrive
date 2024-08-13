import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {QuestionnaireDataViewComponent} from './questionnaire-data-view.component';

describe('QuestionnaireDataViewComponent', () => {
  let component: QuestionnaireDataViewComponent;
  let fixture: MockedComponentFixture<QuestionnaireDataViewComponent>;

  beforeEach(() => {
    return MockBuilder(QuestionnaireDataViewComponent, AppModule).keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(QuestionnaireDataViewComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
