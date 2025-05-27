import {By} from '@angular/platform-browser';
import {customFormlyConfig} from '@app/app.config';
import {HelpWrapperComponent} from '@app/shared/forms/help-wrapper/help-wrapper.component';
import {FormlyModule} from '@ngx-formly/core';
import {keysToCamel} from '@app/shared/utilities/snakeToCamel';
import {MockFormlyFormComponent} from '@app/shared/fixtures/mock-form.component';
import {mockIdentificationQuestionnaireMeta} from '@app/shared/fixtures/mock-identification-questionnaire-meta';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('HelpWrapperComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(HelpWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(
      MockFormlyFormComponent,
      {fields: keysToCamel(mockIdentificationQuestionnaireMeta)},
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(fixture.debugElement.query(By.css('app-help-wrapper'))).toBeTruthy();
  });
});
