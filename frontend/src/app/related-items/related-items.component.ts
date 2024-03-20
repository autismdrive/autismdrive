import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {RelatedOptions} from '../_models/related_results';
import {Resource} from '../_models/resource';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-related-items',
  templateUrl: './related-items.component.html',
  styleUrls: ['./related-items.component.scss'],
})
export class RelatedItemsComponent implements OnInit {
  @Input() resource: Resource;
  @Input() study: Study;
  @Input() loading: boolean;
  @Input() parentComponent: string;
  relatedResources: Resource[] = [];
  relatedStudies: Study[] = [];

  constructor(private api: ApiService, private router: Router, private googleAnalytics: GoogleAnalyticsService) {}

  ngOnInit() {
    const options: RelatedOptions = {
      resource_id: this.resource ? this.resource.id : undefined,
      study_id: this.study ? this.study.id : undefined,
    };
    if (this.resource || this.study) {
      this.api.getRelatedResults(options).subscribe(relatedItems => {
        this.relatedResources = relatedItems.resources;
        this.relatedStudies = relatedItems.studies;
      });
    }
  }

  goResource(resourceId: number) {
    this.googleAnalytics.relatedContentEvent('related_resource', this.parentComponent);
    this.router.navigate(['/resource', resourceId]);
  }

  goStudy(studyId: number) {
    this.googleAnalytics.relatedContentEvent('related_study', this.parentComponent);
    this.router.navigate(['/study', studyId]);
  }
}
