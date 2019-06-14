import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Query, HitLabel } from '../_models/query';

@Component({
  selector: 'app-studies',
  templateUrl: './studies.component.html',
  styleUrls: ['./studies.component.scss']
})
export class StudiesComponent implements OnInit {
  query: Query;

  constructor(private api: ApiService) {
    this.loadStudies();
  }

  ngOnInit() {
  }

  loadStudies() {
    const query = new Query({
      filters: [{field: 'Type', value: HitLabel.STUDY}]
    });
    this.api.search(query).subscribe(q => this.query = q);
  }

}
