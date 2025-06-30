import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatDialog} from '@angular/material/dialog';
import {MatIconModule} from '@angular/material/icon';
import {MatTooltipModule} from '@angular/material/tooltip';
import {ActivatedRoute, Router} from '@angular/router';
import {EditButtonComponent} from '@app/edit-button/edit-button.component';
import {LoadingComponent} from '@app/loading/loading.component';
import {snakeToUpperCase} from '@app/shared/utilities/snakeToUpper';
import {StudyInquiryComponent} from '@app/study-inquiry/study-inquiry.component';
import {StudySurveyEntryComponent} from '@app/study-survey-entry/study-survey-entry.component';
import {Study} from '@models/study';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {MarkdownModule} from 'ngx-markdown';
import {InvestigatorFormComponent} from '../investigator-form/investigator-form.component';

@Component({
  standalone: true,
  selector: 'app-study-detail',
  templateUrl: './study-detail.component.html',
  styleUrls: ['./study-detail.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule,
    EditButtonComponent,
    MarkdownModule,
    FlexModule,
    MatButtonModule,
    MatIconModule,
    MatTooltipModule,
    StudySurveyEntryComponent,
    StudyInquiryComponent,
    LoadingComponent,
  ],
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
        const studyId = params['studyId'] ? parseInt(params['studyId'], 10) : null;

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

  userCanEdit() {
    return (
      this.currentUser &&
      (this.currentUser.permissions.includes('edit_resource') || this.currentUser.permissions.includes('edit_study'))
    );
  }
}
