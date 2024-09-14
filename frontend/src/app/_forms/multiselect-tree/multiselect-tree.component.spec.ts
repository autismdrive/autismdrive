import {AppModule} from '@app/app.module';
import {createFieldComponent} from '@ngx-formly/core/testing';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {of} from 'rxjs';

describe('MultiselectTreeComponent', () => {
  it('should render multi-select tree', () => {
    const {query} = createFieldComponent(
      {
        type: 'multiselecttree',
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

    expect(query('app-multiselect-tree')).not.toBeNull();
  });
});
