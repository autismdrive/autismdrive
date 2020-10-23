import {Component, OnInit, Input} from '@angular/core';
import {StudyCategory} from '../_models/study_category';
import {ResourceCategory} from '../_models/resource_category';
import {AgeRange, Language, Covid19Categories} from '../_models/hit_type';
import {Router} from '@angular/router';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-filter-chips',
  templateUrl: './filter-chips.component.html',
  styleUrls: ['./filter-chips.component.scss']
})
export class FilterChipsComponent implements OnInit {
  @Input() categories: StudyCategory[] | ResourceCategory[] = [];
  @Input() ages: string[] = [];
  @Input() languages: string[] = [];
  @Input() covid19_categories: string[] = [];
  @Input() parentComponent: string;

  ageLabels = AgeRange.labels;
  languageLabels = Language.labels;
  covid19Labels = Covid19Categories.labels;

  constructor(
    private router: Router,
    private googleAnalytics: GoogleAnalyticsService
  ) {
  }

  ngOnInit() {
  }

  goFilter(routerLink, type: string, queryParams) {
    this.googleAnalytics.relatedContentEvent(type, this.parentComponent);
    this.router.navigate(routerLink, queryParams);
  }

}
