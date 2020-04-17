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
  rootValue = '';

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

  hasNoContent = (_: number, _nodeData: Category) => {
    const noContent = _nodeData.name === '' && _nodeData.id === undefined;
    if (_nodeData.name === '') {
      console.log({_nodeData});
    }

    return noContent;
  }

  /** Select the category so we can insert the new item. */
  addNewItem(node: Category) {
    this.dataSource.data = this.insertNewChildNode(node, this.dataSource.data);
    this.refreshTree();
    this.treeControl.expand(node);
  }

  /** Save the node to database */
  saveNode(node: Category, itemValue: string) {
    node.name = itemValue;
    this.api.addCategory(node).subscribe(cat => {
      this.rootValue = '';
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

  cancelDelete() {
    this.showConfirmDelete = false;
    this.nodeToDelete = undefined;
  }

  cancelAdd() {
    this.dataSource.data = this.removeEmpty(this.dataSource.data);
    this.refreshTree();
  }

  private removeEmpty(cats: Category[]): Category[] {
    if (cats && cats.length > 0) {
      cats = cats.filter(c => c.name !== '');
      return cats.map(cat => {
        cat.children = this.removeEmpty(cat.children);
        return cat;
      });
    } else {
      return cats;
    }
  }

  private insertNewChildNode(parentNode: Category, cats: Category[]): Category[] {
    if (cats && cats.length > 0) {
      const parentIndex = cats.findIndex(c => c.id === parentNode.id);
      if (parentIndex !== - 1) {
        cats[parentIndex].children.push({name: '', parent_id: parentNode.id});
        return cats;
      } else {
        return cats.map(cat => {
          cat.children = this.insertNewChildNode(parentNode, cat.children);
          return cat;
        });
      }
    }
  }

  private refreshTree() {
    const _data = this.dataSource.data;
    this.dataSource.data = null;
    this.dataSource.data = _data;
  }
}
