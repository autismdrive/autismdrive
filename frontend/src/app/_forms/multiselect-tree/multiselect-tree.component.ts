import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, OnInit} from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {Observable, of} from 'rxjs';
import {Category} from '../../_models/category';
import {TreeComponent} from '@App/app/_forms/tree/tree.component';

@Component({
  selector: 'app-multiselect-tree',
  templateUrl: './multiselect-tree.component.html',
  styleUrls: ['./multiselect-tree.component.scss'],
})
export class MultiselectTreeComponent extends TreeComponent implements OnInit {
  dataLoaded = false;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  ngOnInit() {
    (this.props.options as Observable<any>).subscribe((categories: Category[]) => {
      this.dataSource.data = categories;
      this.updateSelection();
    });
  }

  updateSelection() {
    if (this.isReady()) {
      if (this.model.categories) {
        (this.model.categories as Category[]).forEach((cat: Category) => {
          const node = this.findNode(cat.id);
          if (node) {
            this.toggleNode(node);
          }
          this._updateModelCategories();
        });
      }
      this.dataLoaded = true;
    }
  }

  hasNestedChild = (_: number, node: Category) => {
    return node.children && node.children.length > 0;
  };

  numSelectedDescendants(node: Category): number {
    const descendants: Category[] = this.treeControl.getDescendants(node);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Toggle the category item selection. Select/deselect all the parent/grandparent nodes */
  toggleNode(node: Category): void {
    this.checklistSelection.toggle(node);
    const ancestors = [];
    let parent = this.findNode(node.parent_id);
    while (parent != null) {
      ancestors.push(parent);
      parent = this.findNode(parent.parent_id);
    }

    if (this.checklistSelection.isSelected(node)) {
      ancestors.forEach(anc => {
        const parentNode = this.findNode(anc.id);
        this.checklistSelection.select(parentNode);
      });
    } else {
      ancestors.forEach(anc => {
        const parentNode = this.findNode(anc.id);
        if (this.numSelectedDescendants(parentNode) < 1) {
          this.checklistSelection.deselect(parentNode);
        }
      });
    }

    this._updateModelCategories();
  }

  isReady(): boolean {
    return !!(this.field && this.field.form && this.field.form.controls);
  }

  private _updateModelCategories() {
    this.model.categories = [];
    this.checklistSelection.selected.forEach(c => (this.model.categories[c.id] = true));
  }
}
