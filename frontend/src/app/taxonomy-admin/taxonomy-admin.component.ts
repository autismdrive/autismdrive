import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {Observable, of} from 'rxjs';
import {Category} from '@models/category';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  selector: 'app-taxonomy-admin',
  templateUrl: './taxonomy-admin.component.html',
  styleUrls: ['./taxonomy-admin.component.scss'],
})
export class TaxonomyAdminComponent {
  treeControl: NestedTreeControl<Category>;
  dataSource: MatTreeNestedDataSource<Category>;
  dataLoaded = false;
  nodes: {[key: number]: Category} = {};
  showConfirmDelete = false;
  nodeToDelete: Category;
  currentUser: User;
  rootValue = '';
  highlightedNode: number;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
  ) {
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
    this.getCategoryTree(true);
  }

  getCategoryTree(updateDisplayOrder = false, done?: () => void) {
    this.api.getCategoryTree().subscribe(async (categories: Category[]) => {
      // Check tree for any categories with missing display_order.
      if (updateDisplayOrder && (await this.hasMissingDisplayOrder(categories))) {
        // Add display order to each category and save it.
        await this.walkTree(categories, (cat, i) => {
          cat.display_order = i;
          return this.api.addCategory(cat);
        }).then(() => {
          this.dataSource.data = categories;
          if (done) {
            done();
          }
        });
      } else {
        // Just walk the tree to update the node index.
        return await this.walkTree(categories, (cat, i) => {
          this.nodes[cat.id] = cat;
          return of(true);
        }).then(() => {
          this.dataSource.data = categories;
          if (done) {
            done();
          }
        });
      }
    });
  }

  hasNestedChild = (_: number, node: Category) => {
    return node.children && node.children.length > 0;
  };

  hasNoContent = (_: number, _nodeData: Category) => {
    const noContent = _nodeData.name === '' && _nodeData.id === undefined;
    if (_nodeData.name === '') {
      console.log({_nodeData});
    }

    return noContent;
  };

  /** Select the category so we can insert the new item. */
  addNewItem(node: Category) {
    this.dataSource.data = this.insertNewChildNode(node, this.dataSource.data);
    this.refreshTree();
    this.treeControl.expand(node);
  }

  /** Save the node to database */
  saveNode(node: Category, itemValue: string) {
    node.name = itemValue;
    this.api.addCategory(node).subscribe(newCat => {
      const newCatId = newCat.id;
      this.rootValue = '';
      this.getCategoryTree(true, () => {
        this.refreshTree();
        this.expandAncestorNodes(newCatId);
        this.highlightedNode = newCatId;
      });
    });
  }

  /** Increments/decrements display order of the given node */
  moveItem(node: Category, direction: number) {
    const nodeId = node.id;
    const oldIndex = node.display_order;

    // Get sibling nodes
    const siblings = node.parent_id === null ? this.dataSource.data : this.nodes[node.parent_id].children;

    // Get index of next/prev node to swap display order with
    const newIndex = node.display_order + direction;

    // Do nothing if...
    if (
      siblings.length <= 1 || // ...there is only one node (or fewer).
      (direction < 0 && newIndex < 0) || // ...decrementing and node is already first.
      (direction > 0 && newIndex === siblings.length) // ...incrementing and node is already last.
    ) {
      return;
    }

    const swapNode = siblings[newIndex];
    swapNode.display_order = oldIndex;
    node.display_order = newIndex;

    this.api.addCategory(swapNode).subscribe(() => {
      this.api.addCategory(node).subscribe(() => {
        this.rootValue = '';
        this.getCategoryTree(false, () => {
          this.refreshTree();
          this.highlightedNode = nodeId;
          this.expandAncestorNodes(nodeId);
        });
      });
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
      if (parentIndex !== -1) {
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

  /** Recursively visits every node in the given tree and executes the given callback on each node */
  private async walkTree(cats: Category[], callback: (c: Category, i: number) => Observable<any>) {
    return cats.map(async (c, i) => {
      // Store node in an index for faster retrieval by id later.
      this.nodes[c.id] = c;

      // Execute the callback.
      const result = callback(c, i);

      // If this node has children, recursively walk them.
      if (c.children && c.children.length > 0) {
        // The callback must return an observable. Wait for the
        // observable to resolve before going through the next level.
        return result.subscribe(async () => {
          return await this.walkTree(c.children, callback);
        });
      }
    });
  }

  /** Returns true if any category in the given category tree is missing the display_order property. */
  private async hasMissingDisplayOrder(categories: Category[]) {
    let noDisplayOrder = false;
    await this.walkTree(categories, (c: Category, i: number) => {
      if (c.display_order === null || c.display_order === undefined) {
        noDisplayOrder = true;
      }

      return of(noDisplayOrder);
    });
    return noDisplayOrder;
  }

  getSiblings(node: Category) {
    if (node.parent_id === null) {
      return this.dataSource.data;
    } else {
      const parent = this.nodes[node.parent_id];
      if (parent && parent.children && parent.children.length >= 0) {
        return parent.children;
      } else {
        return [];
      }
    }
  }

  // Recursively expand ancestor nodes of the given nodeId.
  private expandAncestorNodes(nodeId: number) {
    const newNode = this.nodes[nodeId];
    if (newNode.parent_id !== null) {
      const parent = this.nodes[newNode.parent_id];
      this.treeControl.expand(parent);

      if (parent.parent_id !== null) {
        this.expandAncestorNodes(parent.id);
      }
    }
  }
}
