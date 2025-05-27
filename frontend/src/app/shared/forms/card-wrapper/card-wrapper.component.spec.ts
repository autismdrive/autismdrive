import {By} from '@angular/platform-browser';
import {customFormlyConfig} from '@app/app.config';
import {CardWrapperComponent} from '@app/shared/forms/card-wrapper/card-wrapper.component';
import {FormlyModule} from '@ngx-formly/core';
import {keysToCamel} from '@app/shared/utilities/snakeToCamel';
import {MockFormlyFormComponent} from '@app/shared/fixtures/mock-form.component';
import {mockHousematesQuestionnaireMeta} from '@app/shared/fixtures/mock-housemates-questionnaire-meta';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('CardWrapperComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(CardWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
  });

  beforeEach(() => {
    fixture = MockRender(
      MockFormlyFormComponent,
      {fields: [keysToCamel(mockHousematesQuestionnaireMeta)]},
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(fixture.debugElement.query(By.css('app-card-wrapper'))).toBeTruthy();
  });
});
