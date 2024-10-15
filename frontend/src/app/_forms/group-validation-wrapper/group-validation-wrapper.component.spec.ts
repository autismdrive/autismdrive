import {AppModule} from '@app/app.module';
import {createFieldComponent} from '@ngx-formly/core/testing';

describe('GroupValidationWrapperComponent', () => {
  it('should render group-validation wrapper', () => {
    const {query} = createFieldComponent(
      {
        wrappers: ['group-validation'],
        props: {
          label: 'Name',
          required: true,
          description: 'Name description',
        },
      },
      {
        imports: [AppModule],
      },
    );

    expect(query('app-group-validation-wrapper')).not.toBeNull();
  });
});
