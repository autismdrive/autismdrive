import {SelectionModel} from '@angular/cdk/collections';
import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, OnInit, Renderer2, ViewChild} from '@angular/core';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckbox, MatCheckboxModule} from '@angular/material/checkbox';
import {MatIconModule} from '@angular/material/icon';
import {MatTree, MatTreeModule, MatTreeNestedDataSource} from '@angular/material/tree';
import {Category, CatTreeNode} from '@app/shared/models/category';
import {FieldTypeConfig, FormlyModule} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';
import {lastValueFrom, Observable} from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-multiselect-tree',
  templateUrl: './multiselect-tree.component.html',
  styleUrls: ['./multiselect-tree.component.scss'],
  imports: [
    MatBadgeModule,
    MatCheckboxModule,
    MatIconModule,
    MatButtonModule,
    MatTreeModule,
    CommonModule,
    ReactiveFormsModule,
    FormlyModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MultiselectTreeComponent extends FieldType<FieldTypeConfig> implements OnInit {
  dataSource: MatTreeNestedDataSource<Category>;
  @ViewChild(MatTree) tree: MatTree<Category, string>;
  @ViewChild('categoryCheckbox') checkboxes: MatCheckbox[];

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
  descendantsMap = new Map<number, Category[]>();

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
    this.initializeDescendantsMap();
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

  numSelectedDescendants(category: Category): number {
    const descendants = this.descendantsMap.get(category.id);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Returns a flat list of Categories that have the given category as an ancestor. */
  getDescendants(category: Category, descendants: Category[]) {
    if (!descendants) {
      descendants = [];
    }

    // Recurse through all children and populate the descendants list.
    for (const child of category.children) {
      descendants.push(child);
      this.getDescendants(child, descendants);
    }

    return descendants;
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

  /**
   * Recurse through entire tree, building a map of ids and a list of descendant categories.
   * Do this just once when the tree initializes, so we don't have to update it every time
   * the tree updates.
   **/
  initializeDescendantsMap() {
    const _recurseThroughDescendants = (ancestorCat: Category) => {
      const descendants = [];

      // Recurse through all children of this category and populate its descendants list.
      for (const child of ancestorCat.children) {
        descendants.push(child);
        descendants.concat(_recurseThroughDescendants(child));
      }

      // Through the magic of recursion, the descendants list should now contain just the descendants of the given category.
      this.descendantsMap.set(ancestorCat.id, descendants);
      return descendants;
    };

    // Loop through root-level categories
    for (const cat of this.dataSource.data) {
      _recurseThroughDescendants(cat);
    }
  }
}
