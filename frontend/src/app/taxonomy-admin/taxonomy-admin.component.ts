import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, OnInit} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {of} from 'rxjs';
import {Category} from '../_models/category';
import {ApiService} from '../_services/api/api.service';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/api/authentication-service';

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
  nodeToDelete: Category;
  currentUser: User;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
  ) {
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
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

  showDelete(node: Category) {
    this.showConfirmDelete = true;
    this.nodeToDelete = node;
  }

  deleteNode(node: Category) {
    this.api.deleteCategory(node.id).subscribe(cat => {
      this.showConfirmDelete = false;
      this.nodeToDelete = null;
      this.getCategoryTree();
    });
  }

}
