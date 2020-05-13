import {Component, Input, OnInit} from '@angular/core';
import {Category} from '../_models/category';
import {AgeRange, Covid19Categories, Language} from '../_models/hit_type';

@Component({
  selector: 'app-favorite-topics',
  templateUrl: './favorite-topics.component.html',
  styleUrls: ['./favorite-topics.component.scss']
})
export class FavoriteTopicsComponent implements OnInit {
  @Input() favoriteTopics: Category[] = [];
  @Input() favoriteAges: string[] = [];
  @Input() favoriteLanguages: string[] = [];
  @Input() favoriteCovid19Topics: string[] = [];

  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;

  constructor() { }

  ngOnInit() {
  }

}
