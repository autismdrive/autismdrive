import {AppModule} from '@app/app.module';
import {createFieldComponent} from '@ngx-formly/core/testing';

describe('CardWrapperComponent', () => {
  it('should render card wrapper', () => {
    const {query} = createFieldComponent(
      {
        wrappers: ['card'],
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

    expect(query('app-card-wrapper')).not.toBeNull();
  });
});
