import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Resource } from '../_models/resource';
import { Query, Hit } from '../_models/query';

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
      filters: [{field: 'Type', value: 'RESOURCE'}]
    });
    this.api.search(query).subscribe(q => this.query = q);
  }

}
