import {Component, Input, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {FavoriteTopicsDialogComponent} from '../favorite-topics-dialog/favorite-topics-dialog.component';
import {Category} from '../_models/category';
import {AgeRange, Covid19Categories, Language} from '../_models/hit_type';
import {User} from '../_models/user';
import {UserFavorite} from '../_models/user_favorite';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-favorite-topics',
  templateUrl: './favorite-topics.component.html',
  styleUrls: ['./favorite-topics.component.scss'],
})
export class FavoriteTopicsComponent implements OnInit {
  @Input() currentUser: User;
  favoriteTopics: Category[] = [];
  favoriteAges: string[] = [];
  favoriteLanguages: string[] = [];
  favoriteCovid19Topics: string[] = [];

  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;

  constructor(private api: ApiService, public dialog: MatDialog) {}

  ngOnInit() {
    this.loadFavorites();
  }

  loadFavorites() {
    this.api.getFavoritesByUserAndType(this.currentUser, 'category').subscribe(favorites => {
      this.favoriteTopics = favorites.map(f => f['category']);
    });
    this.api.getFavoritesByUserAndType(this.currentUser, 'age_range').subscribe(favorites => {
      this.favoriteAges = favorites.map(f => f['age_range']);
    });
    this.api.getFavoritesByUserAndType(this.currentUser, 'language').subscribe(favorites => {
      this.favoriteLanguages = favorites.map(f => f['language']);
    });
    this.api.getFavoritesByUserAndType(this.currentUser, 'covid19_category').subscribe(favorites => {
      this.favoriteCovid19Topics = favorites.map(f => f['covid19_category']);
    });
  }

  openFavoriteTopicsDialog(): void {
    const dialogRef = this.dialog.open(FavoriteTopicsDialogComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      data: {
        user: this.currentUser,
        topics: this.favoriteTopics,
        ages: this.favoriteAges,
        languages: this.favoriteLanguages,
        covid19_categories: this.favoriteCovid19Topics,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const favorites: UserFavorite[] = [];
        result.topics.forEach(topic => {
          favorites.push(new UserFavorite({user_id: this.currentUser.id, type: 'category', category_id: topic.id}));
        });
        result.ages.forEach(age => {
          favorites.push(new UserFavorite({user_id: this.currentUser.id, type: 'age_range', age_range: age}));
        });
        result.languages.forEach(language => {
          favorites.push(new UserFavorite({user_id: this.currentUser.id, type: 'language', language: language}));
        });
        result.covid19_categories.forEach(c19 => {
          favorites.push(
            new UserFavorite({user_id: this.currentUser.id, type: 'covid19_category', covid19_category: c19}),
          );
        });
        this.api.addUserFavorites(favorites).subscribe();
        this.favoriteTopics = result.topics;
        this.favoriteAges = result.ages;
        this.favoriteLanguages = result.languages;
        this.favoriteCovid19Topics = result.covid19_categories;
      }
    });
  }
}
