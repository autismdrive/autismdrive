import {Component, Input, OnInit} from '@angular/core';
import {Resource} from '../_models/resource';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {RelatedOptions} from '../_models/related_results';

@Component({
  selector: 'app-related-items',
  templateUrl: './related-items.component.html',
  styleUrls: ['./related-items.component.scss']
})
export class RelatedItemsComponent implements OnInit {
  @Input() resource: Resource;
  @Input() study: Study;
  @Input() loading: boolean;
  relatedResources: Resource[] = [];
  relatedStudies: Study[] = [];

  constructor(private api: ApiService) {
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

}
