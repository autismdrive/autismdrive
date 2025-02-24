import {SelectionModel} from '@angular/cdk/collections';
import {NgForOf} from '@angular/common';
import {Component, Inject, OnInit} from '@angular/core';
import {MatBadge} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckbox} from '@angular/material/checkbox';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatFormField, MatLabel} from '@angular/material/form-field';
import {MatIcon} from '@angular/material/icon';
import {MatOption, MatSelect} from '@angular/material/select';
import {MatTreeModule} from '@angular/material/tree';
import {TreeComponent} from '@app/_forms/tree/tree.component';
import {Category} from '@models/category';
import {AgeRange, Covid19Categories, Language} from '@models/hit_type';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {Observable} from 'rxjs';
import {ResourceDetailComponent} from '../resource-detail/resource-detail.component';

interface TopicOption {
  value: string;
  label: string;
}

@Component({
  standalone: true,
  selector: 'app-favorite-topics-dialog',
  templateUrl: './favorite-topics-dialog.component.html',
  styleUrls: ['./favorite-topics-dialog.component.scss'],
  imports: [
    MatBadge,
    MatButtonModule,
    MatCheckbox,
    MatDialogModule,
    MatFormField,
    MatIcon,
    MatLabel,
    MatOption,
    MatSelect,
    MatTreeModule,
    NgForOf,
  ],
})
export class FavoriteTopicsDialogComponent extends TreeComponent implements OnInit {
  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;
  ageOptions = this.getOptions(this.ageLabels);
  languageOptions = this.getOptions(this.languageLabels);
  covid19Options = this.getOptions(this.covid19Labels);

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

  getOptions(modelLabels: {[key: string]: string}): TopicOption[] {
    return Object.entries(modelLabels).map(([key, label]) => ({value: key, label: label}));
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

  getChildren(node: Category): Category[] | Observable<Category[]> {
    return node.children;
  }

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
