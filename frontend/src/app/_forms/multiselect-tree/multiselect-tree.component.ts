import {SelectionModel} from '@angular/cdk/collections';
import {CommonModule} from '@angular/common';
import {Component, OnInit, ViewChild} from '@angular/core';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatIconModule} from '@angular/material/icon';
import {MatTree, MatTreeModule} from '@angular/material/tree';
import {TreeComponent} from '@app/_forms/tree/tree.component';
import {Category} from '@models/category';
import {Observable} from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-multiselect-tree',
  templateUrl: './multiselect-tree.component.html',
  styleUrls: ['./multiselect-tree.component.scss'],
  imports: [MatBadgeModule, MatCheckboxModule, MatIconModule, MatButtonModule, MatTreeModule, CommonModule],
})
export class MultiselectTreeComponent extends TreeComponent implements OnInit {
  @ViewChild(MatTree) tree: MatTree<Category>;

  dataLoaded = false;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  ngOnInit() {
    console.log('MultiselectTreeComponent > ngOnInit');
    (this.props.options as Observable<any>).subscribe((categories: Category[]) => {
      console.log('MultiselectTreeComponent > ngOnInit > this.props.options.subscribe', categories);
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

  async numSelectedDescendants(category: Category): Promise<number> {
    const catNode = this.findNode(category.id);
    const descendants = await this.getDescendants(catNode);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  /** Toggle the category item selection. Select/deselect all the parent/grandparent nodes */
  async toggleNode(category: Category): Promise<void> {
    this.checklistSelection.toggle(category);
    const ancestors = [];
    let parentNode = this.findNode(category.parent_id);
    while (parentNode != null) {
      ancestors.push(parentNode);
      parentNode = this.findNode(parentNode.data.parent_id);
    }

    if (this.checklistSelection.isSelected(category)) {
      ancestors.forEach(anc => {
        const parentNode = this.findNode(anc.id);
        this.checklistSelection.select(parentNode);
      });
    } else {
      for (const anc of ancestors) {
        const parentNode = this.findNode(anc.id);
        const numSelected = await this.numSelectedDescendants(parentNode);
        if (numSelected < 1) {
          this.checklistSelection.deselect(parentNode);
        }
      }
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
