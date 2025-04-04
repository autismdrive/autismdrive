import {ChangeDetectionStrategy, Component, effect} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {ActivatedRoute, Router} from '@angular/router';
import {Study} from '@models/study';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {snakeToUpperCase} from '@util/snakeToUpper';
import {InvestigatorFormComponent} from '../investigator-form/investigator-form.component';

@Component({
  standalone: true,
  selector: 'app-study-detail',
  templateUrl: './study-detail.component.html',
  styleUrls: ['./study-detail.component.scss'],
  // providers: [ApiService, AuthenticationService],
  changeDetection: ChangeDetectionStrategy.OnPush,
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
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
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
