import {Component, Input} from '@angular/core';
import {User} from '@models/user';
import {UserFavorite} from '@models/user_favorite';
import {ApiService} from '@services/api/api.service';

@Component({
  selector: 'app-favorite-resource-button',
  templateUrl: './favorite-resource-button.component.html',
  styleUrls: ['./favorite-resource-button.component.scss'],
})
export class FavoriteResourceButtonComponent {
  @Input() resource_id: number;
  favorite: UserFavorite;
  @Input() user: User;

  constructor(private api: ApiService) {}

  userFavorite() {
    for (const f of this.user.user_favorites) {
      if (f.resource_id === this.resource_id) {
        return true;
      }
    }
    return false;
  }

  addFavorite() {
    const favorite: UserFavorite[] = [
      new UserFavorite({user_id: this.user.id, resource_id: this.resource_id, type: 'resource'}),
    ];
    this.api.addUserFavorites(favorite).subscribe(f => {
      this.user.user_favorites.push(f[0]);
    });
  }

  deleteFavorite() {
    for (const f of this.user.user_favorites) {
      if (f.resource_id === this.resource_id) {
        this.favorite = f;
      }
    }
    this.api.deleteUserFavorite(this.favorite).subscribe(x => {
      this.user.user_favorites.splice(
        this.user.user_favorites.findIndex(f => f.id === this.favorite.id),
        1,
      );
    });
  }

  handleClick($event) {
    $event.preventDefault();
    $event.stopPropagation();
    if (this.userFavorite()) {
      this.deleteFavorite();
    } else {
      this.addFavorite();
    }
  }

  instructions(): string {
    if (this.userFavorite()) {
      return 'Remove Resource from Profile';
    } else {
      return 'Save Resource to Profile';
    }
  }
}
