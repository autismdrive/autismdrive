import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';
import {AgeRange, Covid19Categories, Language} from '@models/hit_type';
import {ResourceCategory} from '@models/resource_category';
import {StudyCategory} from '@models/study_category';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-filter-chips',
  templateUrl: './filter-chips.component.html',
  styleUrls: ['./filter-chips.component.scss'],
})
export class FilterChipsComponent {
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
    private googleAnalytics: GoogleAnalyticsService,
  ) {}

  goFilter(routerLink, type: string, queryParams) {
    this.googleAnalytics.relatedContentEvent(type, this.parentComponent);
    this.router.navigate(routerLink, queryParams);
  }
}
