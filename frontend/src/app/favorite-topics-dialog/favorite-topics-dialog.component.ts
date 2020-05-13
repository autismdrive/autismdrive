import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {ResourceDetailComponent} from '../resource-detail/resource-detail.component';
import {ResourceCategory} from '../_models/resource_category';
import {User} from '../_models/user';
import {AgeRange, Covid19Categories, Language} from '../_models/hit_type';
import {UserFavorite} from '../_models/user_favorite';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-favorite-topics-dialog',
  templateUrl: './favorite-topics-dialog.component.html',
  styleUrls: ['./favorite-topics-dialog.component.scss']
})
export class FavoriteTopicsDialogComponent implements OnInit {
  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;

  constructor(
    private api: ApiService,
    public dialogRef: MatDialogRef<ResourceDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      user: User,
      topics: ResourceCategory[],
      ages: string[],
      languages: string[],
      covid19_categories: string[],
    }
  ) { }

  ngOnInit() {
  }

  userFavorite(favorite, field) {
    for (const f of this.data.user.user_favorites) {
      if (field === 'category_id' && favorite === f[field]) {
        return true;
      } else if (f[field] && favorite in f[field]) {
        return true;
      }
    }
    return false;
  }

  addTopic(field, value, type) {
    const favorite: UserFavorite[] = [new UserFavorite({'user_id': this.data.user.id, 'type': type })];
    favorite[0][field] = value;
    this.api.addUserFavorites(favorite).subscribe(f => {
      this.data.user.user_favorites.push(f[0]);
    });
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
