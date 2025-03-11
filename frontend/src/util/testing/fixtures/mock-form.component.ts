import {Component} from '@angular/core';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {createFieldComponent} from '@ngx-formly/core/testing';
import {FormlyMatFormFieldModule} from '@ngx-formly/material/form-field';
import {keysToCamel} from '@util/snakeToCamel';
import {mockHousematesQuestionnaireMeta} from '@util/testing/fixtures/mock-housemates-questionnaire-meta';

/**
 * Custom components that inherit from FormlyField are only rendered in the context of a form.
 * To unit-test a custom FormlyField type, pass this MockFormlyFormComponent into your MockBuild and MockRender
 * methods. You will need to query the debugElement of the fixture to access the instance of your custom
 * FormlyField component.
 *
 * ---------------------------------------------- EXAMPLE ----------------------------------------------
 *
 * import {By} from '@angular/platform-browser';
 * import {FormlyConfig} from '@app/app.config';
 * import {RepeatSectionComponent} from '@forms/repeat-section/repeat-section.component';
 * import {FormlyModule} from '@ngx-formly/core';
 * import {MockFormlyFormComponent} from '@util/testing/fixtures/mock-form.component';
 * import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
 *
 * describe('RepeatSectionComponent', () => {
 *   let component: MockFormlyFormComponent;
 *   let fixture: MockedComponentFixture<MockFormlyFormComponent>;
 *
 *   beforeEach(() => {
 *     return MockBuilder(MockFormlyFormComponent)
 *       .keep(FormlyModule.forRoot(FormlyConfig.config))
 *       .keep(RepeatSectionComponent)
 *       .keep(NG_MOCKS_ROOT_PROVIDERS);
 *   });
 *
 *   beforeEach(() => {
 *     fixture = MockRender(MockFormlyFormComponent, null, {detectChanges: true});
 *     component = fixture.point.componentInstance;
 *   });
 *
 *   it('should create', () => {
 *     expect(component).toBeTruthy();
 *     expect(fixture.debugElement.query(By.css('app-repeat-section'))).toBeTruthy();
 *     expect(fixture.debugElement.query(By.css('.repeat-action'))).toBeTruthy();
 *   });
 * });
 *
 */
@Component({
  standalone: true,
  selector: 'app-mock-formly-form-component',
  template: '<formly-form [fields]="fields"></formly-form>',
  imports: [FormlyModule],
})
export class MockFormlyFormComponent {
  fields = [keysToCamel(mockHousematesQuestionnaireMeta)];

  constructor() {}
}
