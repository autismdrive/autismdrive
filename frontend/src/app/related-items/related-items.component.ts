import {NgClass, NgForOf, NgIf} from '@angular/common';
import {Component, Input, OnInit} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MatLineModule} from '@angular/material/core';
import {MatListModule} from '@angular/material/list';
import {Router} from '@angular/router';
import {TypeIconComponent} from '@app/type-icon/type-icon.component';
import {RelatedOptions} from '@models/related_results';
import {Resource} from '@models/resource';
import {Study} from '@models/study';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {TruncateModule} from '@yellowspot/ng-truncate';

@Component({
  standalone: true,
  selector: 'app-related-items',
  templateUrl: './related-items.component.html',
  styleUrls: ['./related-items.component.scss'],
  imports: [
    FlexModule,
    MatCardModule,
    MatLineModule,
    MatListModule,
    NgClass,
    NgForOf,
    NgIf,
    TruncateModule,
    TypeIconComponent,
  ],
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
    private googleAnalytics: GoogleAnalyticsService,
  ) {}

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
