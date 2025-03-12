import {By} from '@angular/platform-browser';
import {FormlyConfig} from '@app/app.config';
import {profileFormFields} from '@app/profile/profile.component';
import {GroupValidationWrapperComponent} from '@forms/group-validation-wrapper/group-validation-wrapper.component';
import {FormlyModule} from '@ngx-formly/core';
import {MockFormlyFormComponent} from '@util/testing/fixtures/mock-form.component';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';

describe('GroupValidationWrapperComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<MockFormlyFormComponent>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(GroupValidationWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS);
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
