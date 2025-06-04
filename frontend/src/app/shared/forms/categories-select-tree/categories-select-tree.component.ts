import {SelectionModel} from '@angular/cdk/collections';
import {CdkTreeNode} from '@angular/cdk/tree';
import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, OnInit, Renderer2, ViewChild, ViewChildren} from '@angular/core';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckbox, MatCheckboxModule} from '@angular/material/checkbox';
import {MatError, MatLabel} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatTree, MatTreeModule, MatTreeNestedDataSource} from '@angular/material/tree';
import {Category} from '@models/category';
import {FieldTypeConfig, FormlyModule} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';
import {lastValueFrom, Observable} from 'rxjs';

export type CatTreeNode = CdkTreeNode<Category, Category>;

@Component({
  standalone: true,
  selector: 'app-categories-select-tree',
  templateUrl: './categories-select-tree.component.html',
  styleUrl: './categories-select-tree.component.scss',
  imports: [
    CommonModule,
    FormlyModule,
    MatBadgeModule,
    MatButtonModule,
    MatCheckboxModule,
    MatIconModule,
    MatTreeModule,
    ReactiveFormsModule,
    MatLabel,
    MatError,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CategoriesSelectTreeComponent extends FieldType<FieldTypeConfig> implements OnInit {
  dataSource: MatTreeNestedDataSource<Category>;
  @ViewChild(MatTree) tree: MatTree<Category, number>;
  @ViewChildren('categoryCheckbox') checkboxes: MatCheckbox[];

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(private renderer2: Renderer2) {
    super();
    this.dataSource = new MatTreeNestedDataSource();
  }

  trackBy = (_: number, node: Category) => this.expansionKey(node);
  expansionKey = (node: Category) => node.id;
  childrenAccessor = (dataNode: Category) => dataNode.children ?? [];
  hasNestedChild = (_: number, node: Category) => node?.children?.length > 0;

  ngOnInit() {
    this.setOptions();
  }

  get nodesMap(): Map<number, CatTreeNode> | null {
    if (!(this.tree && this.tree['_nodes'])) return null;
    return this.tree['_nodes'].value;
  }

  /** Returns the tree node from the tree that matches the given Category ID. */
  findNode(catId: number): CatTreeNode | null {
    return this.nodesMap ? this.nodesMap.get(catId) : null;
  }

  /** Explicitly casts the AbstractControl formControl to a FormControl. */
  get formControlCast(): FormControl {
    return this.formControl as FormControl;
  }

  async setOptions() {
    const options: Category[] | Observable<Category[]> = this.props.options;
    this.dataSource.data = options instanceof Observable ? await lastValueFrom(options) : options;
    this.updateSelection();
    this.form.updateValueAndValidity();
  }

  updateSelection() {
    if (!!this.field?.form?.controls) {
      if (this.model.categories) {
        for (const cat of this.model.categories as Category[]) {
          const node = this.findNode(cat.id);

          if (node) {
            this.toggleNode(node.data);
          }
        }
      }
    }
  }

  /** Toggle the category item selection. */
  toggleNode(category: Category) {
    const cats: number[] = this.model.categories || [];
    const i = cats.findIndex(c => c === category.id);
    if (i === -1) {
      cats.push(category.id);
    } else {
      cats.splice(i, 1);
    }
    this.model.categories = cats;

    this.checklistSelection.toggle(category);
  }

  handleExpand() {
    this.checkboxes.forEach(c => {
      this.renderer2.setAttribute(c._inputElement.nativeElement, 'name', this.field.key.toString());
    });
  }
}
