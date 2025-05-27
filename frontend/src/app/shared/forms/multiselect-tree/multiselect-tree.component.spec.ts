import {HarnessLoader} from '@angular/cdk/testing';
import {TestbedHarnessEnvironment} from '@angular/cdk/testing/testbed';
import {CommonModule} from '@angular/common';
import {ReactiveFormsModule} from '@angular/forms';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatCheckboxHarness} from '@angular/material/checkbox/testing';
import {MatTreeModule} from '@angular/material/tree';
import {MatTreeHarness} from '@angular/material/tree/testing';
import {By} from '@angular/platform-browser';
import {customFormlyConfig} from '@app/app.config';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {withFormlyMaterial} from '@ngx-formly/material';
import {mockCategory} from '@app/shared/fixtures/mock-category';
import {MockFormlyFormComponent} from '@app/shared/fixtures/mock-form.component';
import {MockBuilder, MockedComponentFixture, MockRender, NG_MOCKS_ROOT_PROVIDERS} from 'ng-mocks';
import {of} from 'rxjs';

describe('CategoriesSelectTreeComponent', () => {
  let component: MockFormlyFormComponent;
  let fixture: MockedComponentFixture<any>;
  let loader: HarnessLoader;

  // Expected number of tree nodes
  const numPrimary = 4; // min # of primary nodes
  const minChild = 3; // min # of child nodes
  const maxChild = 7; // min # of child nodes
  const minAll = numPrimary + numPrimary * minChild + numPrimary * minChild * minChild;
  const maxAll = numPrimary + numPrimary * maxChild + numPrimary * maxChild * maxChild;

  const expandAllTreeNodes = async (treeHarness: MatTreeHarness) => {
    // Expand all primary and secondary nodes.
    const primaryNodes = await treeHarness.getNodes({level: 1});
    expect(primaryNodes.length).toEqual(numPrimary);

    for (const primaryNode of primaryNodes) {
      await primaryNode.expand();

      fixture.detectChanges();
      await fixture.whenStable();
    }

    const secondaryNodes = await treeHarness.getNodes({level: 2});
    expect(secondaryNodes.length).toBeGreaterThanOrEqual(numPrimary * minChild);
    expect(secondaryNodes.length).toBeLessThanOrEqual(numPrimary * maxChild);

    for (const secondaryNode of secondaryNodes) {
      await secondaryNode.expand();

      fixture.detectChanges();
      await fixture.whenStable();
    }
  };

  beforeEach(() => {
    return MockBuilder(MockFormlyFormComponent)
      .keep(CommonModule)
      .keep(FormlyModule)
      .keep(MatCheckboxModule)
      .keep(MatTreeModule)
      .keep(ReactiveFormsModule)
      .keep(FormlyModule.forRoot(customFormlyConfig))
      .keep(NG_MOCKS_ROOT_PROVIDERS)
      .provide(provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]));
  });

  beforeEach(() => {
    fixture = MockRender(
      MockFormlyFormComponent,
      {
        fields: [
          {
            key: 'category',
            type: 'categorytree',
            props: {
              label: 'Categories',
              required: true,
              options: of([mockCategory]),
              valueProp: 'id',
              labelProp: 'name',
            },
          },
        ],
      },
      {detectChanges: true},
    );
  });

  beforeEach(async () => {
    fixture.detectChanges();
    await fixture.whenStable();
    await fixture.whenRenderingDone();
    component = fixture.point.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);
  });

  it('should create', async () => {
    await fixture.whenStable();

    expect(component).toBeTruthy();
    const componentElement = fixture.debugElement.query(By.css('app-categories-select-tree'));
    expect(componentElement).toBeTruthy();

    const treeElement = componentElement.query(By.css('.mat-tree-node'));
    expect(treeElement).toBeTruthy();
  });

  it('should render checkboxes', async () => {
    await fixture.whenStable();
    const checkboxElements = fixture.debugElement.queryAll(By.css('input[type="checkbox"]'));
    expect(checkboxElements.length).toBeGreaterThanOrEqual(minAll);
    expect(checkboxElements.length).toBeLessThanOrEqual(maxAll);
  });

  it('should render all descendants of a node', async () => {
    await fixture.whenStable();
    const treeHarness = await loader.getHarness(MatTreeHarness);
    await expandAllTreeNodes(treeHarness);

    const checkboxes = fixture.debugElement.queryAll(By.css('input[type="checkbox"]'));
    expect(checkboxes.length).toBeGreaterThanOrEqual(minAll);
    expect(checkboxes.length).toBeLessThanOrEqual(maxAll);
  });

  it('should require at least one category to be checked', async () => {
    await fixture.whenStable();
    const treeHarness = await loader.getHarness(MatTreeHarness);
    const checkboxesHarness = await loader.getAllHarnesses(MatCheckboxHarness);

    // The form should be valid
    const formControl = component.fields[0].formControl;
    const form = formControl.parent;
    expect(formControl).toBeTruthy();
    expect(form).toBeTruthy();

    // Expand all primary and secondary nodes.
    await expandAllTreeNodes(treeHarness);
    expect(form.valid).toBeFalsy();
    expect(formControl.valid).toBeFalsy();

    // Click all checkboxes
    for (const checkbox of checkboxesHarness) {
      await checkbox.check();
      const inputElement = await checkbox.host();
      const catId = await inputElement.getAttribute('id');

      expect(component.fields[0].model.categories).toContain(catId);

      form.updateValueAndValidity();
      expect(form.valid).toBeTruthy();
      expect(formControl.valid).toBeTruthy();
    }
  });
});
