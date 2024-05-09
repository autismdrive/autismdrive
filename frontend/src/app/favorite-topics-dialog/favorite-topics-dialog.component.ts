import {SelectionModel} from '@angular/cdk/collections';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {ResourceDetailComponent} from '../resource-detail/resource-detail.component';
import {Category} from '../_models/category';
import {AgeRange, Covid19Categories, Language} from '../_models/hit_type';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {TreeComponent} from '@app/_forms/tree/tree.component';

@Component({
  selector: 'app-favorite-topics-dialog',
  templateUrl: './favorite-topics-dialog.component.html',
  styleUrls: ['./favorite-topics-dialog.component.scss'],
})
export class FavoriteTopicsDialogComponent extends TreeComponent implements OnInit {
  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;
  ageOptions = this.getOptions(this.ageLabels);
  languageOptions = this.getOptions(this.languageLabels);
  covid19Options = this.getOptions(this.covid19Labels);

  nodes = {};

  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);

  constructor(
    private api: ApiService,
    public dialogRef: MatDialogRef<ResourceDetailComponent>,
    @Inject(MAT_DIALOG_DATA)
    public data: {
      user: User;
      topics: Category[];
      ages: string[];
      languages: string[];
      covid19_categories: string[];
    },
  ) {
    super();
  }

  ngOnInit() {
    this.api.getCategoryTree().subscribe((categories: Category[]) => {
      this.dataSource.data = categories;
      this.updateTopicSelection();
    });
  }

  getOptions(modelLabels) {
    const opts = [];
    for (const key in modelLabels) {
      if (modelLabels.hasOwnProperty(key)) {
        opts.push({value: key, label: modelLabels[key]});
      }
    }
    return opts;
  }

  updateTopicSelection() {
    if (this.data.topics) {
      this.data.topics.forEach(cat => {
        const node = this.findNode(cat.id);
        if (node) {
          this.toggleNode(node);
        }
        this._updateModelCategories();
      });
    }
  }

  /** Toggle the category item selection. */
  toggleNode(node: Category): void {
    this.checklistSelection.toggle(node);
    this._updateModelCategories();
  }

  hasNestedChild = (_: number, node: Category) => {
    return node.children && node.children.length > 0;
  };

  numSelectedDescendants(node: Category): number {
    const descendants: Category[] = this.treeControl.getDescendants(node);
    const selectedDescendants = descendants.filter(d => this.checklistSelection.isSelected(d));
    return selectedDescendants.length;
  }

  private _updateModelCategories() {
    this.data.topics = [];
    this.checklistSelection.selected.forEach(c => this.data.topics.push(c));
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
