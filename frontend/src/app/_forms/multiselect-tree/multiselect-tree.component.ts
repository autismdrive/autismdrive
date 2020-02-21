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
      this.updateSelection();
    });
  }


  updateSelection() {
    if (this.isReady()) {
      if (this.model.categories) {
        this.model.categories.forEach(cat => {
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

  findNode(cat_id: number) {
    const allNodes = [];

    this.dataSource.data.forEach(dataCat => {
      const descendants = this.treeControl.getDescendants(dataCat);
      descendants.forEach(d => allNodes.push(d));
      allNodes.push(dataCat);

    });
    return allNodes.find(i => i.id === cat_id);
  }

  hasNestedChild = (_: number, node: Category) => {
    return (node.children && (node.children.length > 0));
  }

  numSelectedDescendants(node: Category): number {
    const descendants: Category[] = this.treeControl.getDescendants(node);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Toggle the category item selection. Select/deselect all the parent/grandparent nodes */
  toggleNode(node: Category): void {
    this.checklistSelection.toggle(node);
    let ancestors = [];
    let parent = this.findNode(node.parent_id);
    while (parent != null) {
      ancestors.push(parent);
      parent = this.findNode(parent.parent_id)
    }

    if (this.checklistSelection.isSelected(node)) {
      ancestors.forEach(anc => {
        const parentNode = this.findNode(anc.id);
        this.checklistSelection.select(parentNode)
      });
    } else {
      ancestors.forEach(anc => {
        const parentNode = this.findNode(anc.id);
        if (this.numSelectedDescendants(parentNode) < 1) {
          this.checklistSelection.deselect(parentNode)
        }
      })
    }

    this._updateModelCategories();
  }

  isReady(): boolean {
    return !!(
      this.field &&
      this.field.form &&
      this.field.form.controls
    );
  }

  private _updateModelCategories() {
    this.model.categories = [];
    this.checklistSelection.selected.forEach(c => this.model.categories[c.id] = true);
  }
}
