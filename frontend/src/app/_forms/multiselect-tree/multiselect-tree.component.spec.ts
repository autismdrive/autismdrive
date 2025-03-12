import {provideNativeDateAdapter} from '@angular/material/core';
import {By} from '@angular/platform-browser';
import {FormlyConfig} from '@app/app.config';
import {CardWrapperComponent} from '@forms/card-wrapper/card-wrapper.component';
import {MultiselectTreeComponent} from '@forms/multiselect-tree/multiselect-tree.component';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {mockCategory} from '@util/testing/fixtures/mock-category';
import {MockFormlyFormComponent} from '@util/testing/fixtures/mock-form.component';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';

describe('MultiselectTreeComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<any>;

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyMaterialModule)
      .keep(FormlyMatDatepickerModule)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(MultiselectTreeComponent)
      .keep(CardWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideNativeDateAdapter());
  });

  beforeEach(() => {
    fixture = MockRender(
      MockFormlyFormComponent,
      {
        fields: [
          {
            key: 'categories',
            type: 'multiselecttree',
            props: {
              label: 'Topics',
              description: 'This field is required',
              options: of([mockCategory]),
              valueProp: 'id',
              labelProp: 'name',
            },
            hideExpression: '!model.type',
          },
        ],
      },
      {detectChanges: true},
    );
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    fixture.whenStable().then(() => {
      expect(fixture.debugElement.query(By.css('app-multiselect-tree'))).toBeTruthy();
      expect(fixture.debugElement.query(By.css('.mat-tree-node'))).toBeTruthy();
    })
  });
});
