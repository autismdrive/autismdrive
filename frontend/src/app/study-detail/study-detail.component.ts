import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Study } from '../_models/study';
import { User } from '../_models/user'
import { ActivatedRoute, Router } from '@angular/router';
import { snakeToUpperCase } from '../../util/snakeToUpper';
import { AuthenticationService } from '../_services/api/authentication-service';

@Component({
  selector: 'app-study-detail',
  templateUrl: './study-detail.component.html',
  styleUrls: ['./study-detail.component.scss']
})
export class StudyDetailComponent implements OnInit {
  study: Study;
  loading = true;
  currentUser: User;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute, private router: Router,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.route.params.subscribe(params => {
      this.loading = true;
      const studyId = params.studyId ? parseInt(params.studyId, 10) : null;

      if (isFinite(studyId)) {
        this.api.getStudy(studyId).subscribe(study => {
          this.study = study;
          this.loading = false;
        });
      }
    });
  }

  ngOnInit() {
  }

  get snakeToUpperCase() { return snakeToUpperCase; }
}
