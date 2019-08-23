import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Study } from '../_models/study';
import { ActivatedRoute, Router } from '@angular/router';
import { snakeToUpperCase } from '../../util/snakeToUpper';

@Component({
  selector: 'app-study-detail',
  templateUrl: './study-detail.component.html',
  styleUrls: ['./study-detail.component.scss']
})
export class StudyDetailComponent implements OnInit {
  study: Study;

  constructor(private api: ApiService, private route: ActivatedRoute, private router: Router) {
    this.route.params.subscribe(params => {
      const studyId = params.studyId ? parseInt(params.studyId, 10) : null;

      if (isFinite(studyId)) {
        this.api.getStudy(studyId).subscribe(study => {
          this.study = study;
        });
      }
    });
  }

  ngOnInit() {
  }

  get snakeToUpperCase() { return snakeToUpperCase; }
}
