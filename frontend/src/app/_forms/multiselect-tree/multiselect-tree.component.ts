import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, Input, OnInit} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {FormlyTemplateOptions} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';
import {Observable, of} from 'rxjs';
import {Category} from '../../_models/category';

@Component({
  selector: 'app-multiselect-tree',
  templateUrl: './multiselect-tree.component.html',
  styleUrls: ['./multiselect-tree.component.scss']
})
export class MultiselectTreeComponent extends FieldType implements OnInit {
  @Input() to: FormlyTemplateOptions;
  categories: Category[] = [];
  treeControl: NestedTreeControl<Category>;
  dataSource: MatTreeNestedDataSource<Category>;
  dataLoaded = false;
  nodes = {};

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor() {
    super();
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
  }

  ngOnInit() {
    (this.to.options as Observable<any>).subscribe((categories: Category[]) => {
      this.dataSource.data = categories;
      this.categories = categories;
      this.updateSelection();
    });
  }

  updateSelection() {
    if (this.isReady()) {
      this.model.categories.forEach((isSelected, i) => {
        if (isSelected === true) {
          this.checklistSelection.select(i);
        }
      });

      this.dataLoaded = true;
    }
  }

  hasNestedChild = (_: number, node: Category) => {
    return (node.children && (node.children.length > 0));
  }

  getChildren = (node: Category): Category[] => node.children;

  /** Whether all the descendants of the node are selected */
  descendantsAllSelected(node: Category): boolean {
    const descendants = this.treeControl.getDescendants(node);
    return descendants.every(child => this.checklistSelection.isSelected(child));
  }

  /** Whether part of the descendants are selected */
  descendantsPartiallySelected(node: Category): boolean {
    const descendants = this.treeControl.getDescendants(node);
    const result = descendants.some(child => this.checklistSelection.isSelected(child));
    return result && !this.descendantsAllSelected(node);
  }

  numSelectedDescendants(node: Category): number {
    const descendants: Category[] = this.treeControl.getDescendants(node);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Toggle the to-do item selection. Select/deselect all the descendants node */
  toggleNode(node: Category): void {
    this.checklistSelection.toggle(node);
    const descendants = this.treeControl.getDescendants(node);
    this.checklistSelection.isSelected(node)
      ? this.checklistSelection.select(...descendants)
      : this.checklistSelection.deselect(...descendants);

    this._updateModelCategories();
  }

  isReady(): boolean {
    return !!(
      this.field &&
      this.field.form &&
      this.field.form.controls
    );
  }

  hasChild = (_: number, node: Category) => !!node.children && node.children.length > 0;

  /** Toggle the to-do item selection. Select/deselect all the descendants node */
  toggleParentNode(node: Category): void {
    this.checklistSelection.toggle(node);
    const descendants = this.treeControl.getDescendants(node);
    this.checklistSelection.isSelected(node)
      ? this.checklistSelection.select(...descendants)
      : this.checklistSelection.deselect(...descendants);

    // Force update for the parent
    descendants.every(child =>
      this.checklistSelection.isSelected(child)
    );

    this._updateModelCategories();
  }

  private _updateModelCategories() {
    this.checklistSelection.selected.forEach(c => this.model.categories[c.id] = true);
  }
}
