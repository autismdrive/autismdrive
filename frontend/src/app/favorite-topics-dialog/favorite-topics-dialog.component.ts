import {SelectionModel} from '@angular/cdk/collections';
import {CommonModule} from '@angular/common';
import {Component, Inject, OnInit} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatSelectModule} from '@angular/material/select';
import {MatTreeModule} from '@angular/material/tree';
import {Category} from '@models/category';
import {AgeRange, Covid19Categories, Language} from '@models/hit_type';
import {User} from '@models/user';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {ResourceDetailComponent} from '../resource-detail/resource-detail.component';

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
    FormlyModule,
    ReactiveFormsModule,
  ],
})
export class FavoriteTopicsDialogComponent implements OnInit {
  /** The selection for checklist */
  checklistSelection = new SelectionModel<Category>(true /* multiple */);
  form = new FormGroup({});
  fields: FormlyFieldConfig[];

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
  ) {}

  ngOnInit() {
    this.fields = [
      {
        key: 'topics',
        type: 'categorytree',
        props: {
          label: 'Topics',
          options: this.api.getCategoryTree(),
          valueProp: 'id',
          labelProp: 'name',
        },
      },
      {
        key: 'ages',
        type: 'multicheckbox',
        props: {
          label: 'Ages',
          options: AgeRange.options,
        },
      },
      {
        key: 'languages',
        type: 'multicheckbox',
        props: {
          label: 'Languages',
          options: Language.options,
        },
      },
      {
        key: 'covid19_categories',
        type: 'multicheckbox',
        props: {
          label: 'COVID-19 Categories',
          options: Covid19Categories.options,
        },
      },
    ];
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
