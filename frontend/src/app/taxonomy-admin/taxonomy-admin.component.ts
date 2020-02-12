import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, OnInit} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {Observable, of} from 'rxjs';
import {Category} from '../_models/category';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-taxonomy-admin',
  templateUrl: './taxonomy-admin.component.html',
  styleUrls: ['./taxonomy-admin.component.scss']
})
export class TaxonomyAdminComponent implements OnInit {
  categories: Category[] = [];
  treeControl: NestedTreeControl<Category>;
  dataSource: MatTreeNestedDataSource<Category>;
  dataLoaded = false;
  nodes = {};

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(
    private api: ApiService
  ) {
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
  }

  ngOnInit() {
    this.api.getCategoryTree().subscribe((categories: Category[]) => {
      this.dataSource.data = categories;
      this.categories = categories;
      this.updateSelection();
    });
  }

  updateSelection() {
    // if (this.isReady()) {
      // if (this.model.categories) {
      //   this.model.categories.forEach(cat => {
      //     const node = this.findNode(cat);
      //     if (node) {
      //       this.checklistSelection.toggle(node);
      //     }
      //     this._updateModelCategories();
      //   });
      // }
      this.dataLoaded = true;
    // }
  }

  findNode(cat: Category) {
    const allNodes = [];

    this.dataSource.data.forEach(dataCat => {
      const descendants = this.treeControl.getDescendants(dataCat);
      descendants.forEach(d => allNodes.push(d));
      allNodes.push(dataCat);

    });
    return allNodes.find(i => i.id === cat.id);
  }

  hasNestedChild = (_: number, node: Category) => {
    return (node.children && (node.children.length > 0));
  }

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

  // isReady(): boolean {
  //   return !!(
  //     this.field &&
  //     this.field.form &&
  //     this.field.form.controls
  //   );
  // }

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
    // this.model.categories = [];
    // this.checklistSelection.selected.forEach(c => this.model.categories[c.id] = true);
  }

  hasNoContent = (_: number, _nodeData: Category) => _nodeData.name === '';

  /** Select the category so we can insert the new item. */
  addNewItem(node: Category) {
    this.api.addCategory({'name': '', 'parent': node}).subscribe();
    // const data = this.dataSource.data;
    // data.push({'name': '', 'parent': node});
    // this.dataSource.data = data;
    this.treeControl.expand(node);
  }

  /** Save the node to database */
  saveNode(node: Category, itemValue: string) {
    // const nestedNode = this.flatNodeMap.get(node);
    // this._database.updateItem(nestedNode!, itemValue);
    node.name = itemValue;
    this.api.updateCategory(node).subscribe();
  }
}
