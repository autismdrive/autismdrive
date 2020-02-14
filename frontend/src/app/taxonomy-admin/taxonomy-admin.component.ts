import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, OnInit} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {of} from 'rxjs';
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
  showConfirmDelete = false;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(
    private api: ApiService
  ) {
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
    this.getCategoryTree();
  }

  ngOnInit() {
  }

  getCategoryTree() {
    this.api.getCategoryTree().subscribe((categories: Category[]) => {
      this.dataSource.data = categories;
    });
  }

  hasNestedChild = (_: number, node: Category) => {
    return (node.children && (node.children.length > 0));
  };

  numSelectedDescendants(node: Category): number {
    const descendants: Category[] = this.treeControl.getDescendants(node);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Toggle the category item selection. Select/deselect all the descendants node */
  toggleNode(node: Category): void {
    this.checklistSelection.toggle(node);
    const descendants = this.treeControl.getDescendants(node);
    this.checklistSelection.isSelected(node)
      ? this.checklistSelection.select(...descendants)
      : this.checklistSelection.deselect(...descendants);
  }

  hasNoContent = (_: number, _nodeData: Category) => _nodeData.name === '';

  /** Select the category so we can insert the new item. */
  addNewItem(node: Category) {
    const data = this.dataSource.data;
    data.push({'name': '', 'parent': node, 'parent_id': node.id});
    this.dataSource.data = data;
    this.treeControl.expand(node);
    const el: HTMLElement = document.querySelector('.global-footer');
    window.scroll(0, el.offsetTop);
  }

  /** Save the node to database */
  saveNode(node: Category, itemValue: string) {
    node.name = itemValue;
    this.api.addCategory(node).subscribe(cat => {
      this.treeControl.collapseAll();
      this.getCategoryTree();
      window.scroll(0, 0);
    });
  }

  showDelete() {
    this.showConfirmDelete = true;
  }

  onDelete() {
    let itemsProcessed = 0;
    this.checklistSelection.selected.forEach((cat, index, array) => {
      this.api.deleteCategory(cat.id).subscribe(cat => {
        itemsProcessed++;
        if (itemsProcessed === array.length) {
          this.treeControl.collapseAll();
          this.getCategoryTree();
          window.scroll(0, 0);
        }
      });
    });
  }

}
