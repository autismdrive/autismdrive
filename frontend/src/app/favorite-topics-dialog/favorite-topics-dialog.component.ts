import {SelectionModel} from '@angular/cdk/collections';
import {CommonModule, NgForOf, NgIf} from '@angular/common';
import {Component, Inject, OnInit} from '@angular/core';
import {MatBadge, MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckbox, MatCheckboxModule} from '@angular/material/checkbox';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatFormField, MatFormFieldModule, MatLabel} from '@angular/material/form-field';
import {MatIcon, MatIconModule} from '@angular/material/icon';
import {MatOption, MatSelect, MatSelectModule} from '@angular/material/select';
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
    MatBadgeModule,
    MatButtonModule,
    MatCheckboxModule,
    MatDialogModule,
    MatFormFieldModule,
    MatIconModule,
    MatSelectModule,
    MatTreeModule,
    CommonModule,
  ],
})
export class FavoriteTopicsDialogComponent extends TreeComponent implements OnInit {
  ageOptions = AgeRange.options;
  languageOptions = Language.options;
  covid19Options = Covid19Categories.options;

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
