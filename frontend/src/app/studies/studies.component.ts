import { Component, OnInit } from '@angular/core';
import { Study } from '../study';
import { ApiService } from '../services/api/api.service';

@Component({
  selector: 'app-studies',
  templateUrl: './studies.component.html',
  styleUrls: ['./studies.component.scss']
})
export class StudiesComponent implements OnInit {
  studies: Study[];

  constructor(private api: ApiService) {
    this.loadStudies();
  }

  ngOnInit() {
  }

  loadStudies() {
    this.api.getStudies().subscribe(studies => this.studies = studies);
  }

}
