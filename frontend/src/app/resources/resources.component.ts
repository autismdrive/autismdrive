import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Query, HitType } from '../_models/query';

@Component({
  selector: 'app-resources',
  templateUrl: './resources.component.html',
  styleUrls: ['./resources.component.scss']
})
export class ResourcesComponent implements OnInit {
  query: Query;

  constructor(
    private api: ApiService
  ) {
    this.loadResources();
  }

  ngOnInit() {
  }

  loadResources() {
    const query = new Query({
      filters: [{field: 'Type', value: HitType.RESOURCE}]
    });
    this.api.search(query).subscribe(q => this.query = q);
  }

}
