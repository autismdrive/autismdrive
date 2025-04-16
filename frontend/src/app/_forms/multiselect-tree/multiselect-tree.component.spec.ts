import {CDK_TREE_NODE_OUTLET_NODE, CdkNestedTreeNode, CdkTree, CdkTreeNodeOutlet} from '@angular/cdk/tree';
import {ChangeDetectorRef, ElementRef, ViewChild} from '@angular/core';
import {provideNativeDateAdapter} from '@angular/material/core';
import {MatTreeModule, MatTreeNode, MatTreeNodeOutlet} from '@angular/material/tree';
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
  class MockChangeDetectorRef extends ChangeDetectorRef {
    markForCheck() {}
    detach() {}
    detectChanges() {}
    checkNoChanges() {}
    reattach() {}
  }

  class MockElementRef extends ElementRef {}

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(FormlyMaterialModule)
      .keep(FormlyMatDatepickerModule)
      .keep(FormlyModule.forRoot(FormlyConfig.config))
      .keep(MultiselectTreeComponent)
      .keep(CardWrapperComponent)
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .keep(MatTreeModule)
      .provide(CdkTree)
      .provide(ViewChild)
      .provide({provide: CdkNestedTreeNode, useValue: MatTreeNode})
      .provide({provide: CDK_TREE_NODE_OUTLET_NODE, useValue: MatTreeNodeOutlet})
      .provide({provide: CdkTreeNodeOutlet, useValue: MatTreeNodeOutlet})
      .provide({provide: ChangeDetectorRef, useClass: MockChangeDetectorRef})
      .provide({provide: ElementRef, useClass: MockElementRef})
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
    });
  });
});
