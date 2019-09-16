import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import {Query} from '../_models/query';
import {HitType} from '../_models/hit_type';

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
      types: [HitType.STUDY.name]
    });
    this.api.search(query).subscribe(q => this.query = new Query(q));
  }

}
