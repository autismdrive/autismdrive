import {Component, Input} from '@angular/core';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatIconModule} from '@angular/material/icon';
import {MatTreeModule} from '@angular/material/tree';
import {FieldConfigCamelCase} from '@models/questionnaire_meta';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';

/**
 * Custom components that inherit from FormlyField are only rendered in the context of a form.
 * To unit-test a custom FormlyField type, pass this MockFormlyFormComponent into your MockBuild and MockRender
 * methods. You will need to query the debugElement of the fixture to access the instance of your custom
 * FormlyField component.
 *
 * ---------------------------------------------- EXAMPLE ----------------------------------------------
 *
 * import {By} from '@angular/platform-browser';
 * import {customFormlyConfig} from '@app/app.config';
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
 *       .keep(RepeatSectionComponent)
 *       .keep(FormlyModule.forRoot(customFormlyConfig))
 *       .keep(NG_MOCKS_ROOT_PROVIDERS)
 *       .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]));
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
  imports: [
    FormlyMatDatepickerModule,
    FormlyMaterialModule,
    FormlyModule,
    MatBadgeModule,
    MatButtonModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatIconModule,
    MatTreeModule,
  ],
})
export class MockFormlyFormComponent {
  @Input() fields: FormlyFieldConfig[] | FieldConfigCamelCase[];

  constructor() {}
}
