import {createFieldComponent} from '@ngx-formly/core/testing';

describe('HelpWrapperComponent', () => {
  it('should render help wrapper', () => {
    const {query} = createFieldComponent(
      {
        wrappers: ['help'],
        props: {
          label: 'Name',
          required: true,
          description: 'Name description',
        },
      },
      {},
    );

    expect(query('app-help-wrapper')).not.toBeNull();
  });
});
