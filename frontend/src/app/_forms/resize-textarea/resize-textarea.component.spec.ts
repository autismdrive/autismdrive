import {AppModule} from '@app/app.module';
import {createFieldComponent} from '@ngx-formly/core/testing';

describe('ResizeTextareaComponent', () => {
  it('should render resizable textarea field', () => {
    const {query} = createFieldComponent(
      {
        key: 'some_field_key',
        type: 'textarea-auto-resize',
        props: {
          label: 'Some Field Label',
          placeholder: 'This is the placeholder for this field',
          cols: 200,
          rows: 20,
        },
      },
      {
        imports: [AppModule],
      },
    );

    expect(query('app-resize-textarea')).not.toBeNull();
  });
});
