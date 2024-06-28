import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {ActivatedRoute, Router} from '@angular/router';
import {snakeToUpperCase} from '@util/snakeToUpper';
import {Study} from '../_models/study';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {InvestigatorFormComponent} from '../investigator-form/investigator-form.component';

@Component({
  selector: 'app-study-detail',
  templateUrl: './study-detail.component.html',
  styleUrls: ['./study-detail.component.scss'],
})
export class StudyDetailComponent {
  study: Study;
  loading = true;
  currentUser: User;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
    public dialog: MatDialog,
  ) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
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

  get snakeToUpperCase() {
    return snakeToUpperCase;
  }

  openDialog(si): void {
    const dialogRef = this.dialog.open(InvestigatorFormComponent, {
      width: `${window.innerWidth}px`,
      data: {
        si: si,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        si.investigator = result;
        this.api.updateInvestigator(si.investigator).subscribe();
      }
    });
  }
}
