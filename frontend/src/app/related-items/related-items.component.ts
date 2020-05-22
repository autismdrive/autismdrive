import {Component, Input, OnInit} from '@angular/core';
import {Resource} from '../_models/resource';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {RelatedOptions} from '../_models/related_results';
import {Router} from '@angular/router';
import {GoogleAnalyticsService} from '../google-analytics.service';

@Component({
  selector: 'app-related-items',
  templateUrl: './related-items.component.html',
  styleUrls: ['./related-items.component.scss']
})
export class RelatedItemsComponent implements OnInit {
  @Input() resource: Resource;
  @Input() study: Study;
  @Input() loading: boolean;
  @Input() parentComponent: string;
  relatedResources: Resource[] = [];
  relatedStudies: Study[] = [];

  constructor(
    private api: ApiService,
    private router: Router,
    private googleAnalytics: GoogleAnalyticsService
    ) {
  }

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

  goFirstResource() {
    this.googleAnalytics.relatedContentEvent('related_resource', this.parentComponent);
    this.router.navigate(['/resource', this.relatedResources[0].id]);
  }

  goFirstStudy() {
    this.googleAnalytics.relatedContentEvent('related_study', this.parentComponent);
    this.router.navigate(['/study', this.relatedStudies[0].id]);
  }

}
