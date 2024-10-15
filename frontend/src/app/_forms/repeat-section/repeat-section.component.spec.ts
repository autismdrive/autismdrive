import {AppModule} from '@app/app.module';
import {createFieldComponent} from '@ngx-formly/core/testing';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {of} from 'rxjs';

describe('RepeatSectionComponent', () => {
  it('should render repeat section', () => {
    const {query} = createFieldComponent(
      {
        type: 'repeat',
        props: {
          label: 'Topics',
          description: 'This field is required',
          options: of([mockCategory]),
          valueProp: 'id',
          labelProp: 'name',
        },
      },
      {
        imports: [AppModule],
      },
    );

    expect(query('app-repeat-section')).not.toBeNull();
  });
});
