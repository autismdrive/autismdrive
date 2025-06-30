import {By} from '@angular/platform-browser';
import {customFormlyConfig} from '@app/app.config';
import {profileFormFields} from '@app/profile/profile.component';
import {MockFormlyFormComponent} from '@app/shared/fixtures/mock-form.component';
import {GroupValidationWrapperComponent} from '@app/shared/forms/group-validation-wrapper/group-validation-wrapper.component';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('GroupValidationWrapperComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(GroupValidationWrapperComponent)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]));
  });

  beforeEach(() => {
    fixture = MockRender(MockFormlyFormComponent, {fields: profileFormFields}, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(fixture.debugElement.query(By.css('app-group-validation-wrapper'))).toBeTruthy();
  });
});
