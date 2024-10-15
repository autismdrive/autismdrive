import {FormlyFieldConfig} from '@ngx-formly/core';
import {createFieldComponent} from '@ngx-formly/core/testing';
import {FormlyMatFormFieldModule} from '@ngx-formly/material/form-field';

/**
 * Custom components that inherit from FormlyField are only rendered in the context of a form.
 * To unit-test a custom FormlyField type, pass this MockFormComponent into your MockBuild and MockRender
 * methods, then add your custom type to the .forRoot method of the FormlyModule. You will need to query
 * the debugElement of the fixture to access the instance of your custom FormlyField component.
 *
 * ---------------------------------------------- EXAMPLES ----------------------------------------------
 *
 * Custom wrapper:
 *
 * describe('custom-wrapper: Formly Field Wrapper', () => {
 *   it('should render form-field wrapper', () => {
 *     const { query } = renderMockFormlyComponent({
 *       wrappers: ['custom-wrapper'],
 *       props: {
 *         label: 'Name',
 *         required: true,
 *         description: 'Name description',
 *       },
 *     });
 *
 *     expect(query('formly-wrapper-custom-wrapper')).not.toBeNull();
 *
 *     // ...etc...
 *   });
 * });
 *
 *
 * Custom field type:
 *
 * describe('custom-type: Custom Formly Field Type', () => {
 *   it('should render form-field type', () => {
 *     const { query } = renderMockFormlyComponent({
 *       key: 'custom-type',
 *       type: 'custom-type',
 *     });
 *
 *     expect(query('formly-form-field')).not.toBeNull();
 *
 *     // ...etc...
 *   });
 * });
 *
 *
 */
export const renderMockFormlyComponent = (field: FormlyFieldConfig) => {
  return createFieldComponent(field, {
    imports: [FormlyMatFormFieldModule],
  });
};
