import {NgIf} from '@angular/common';
import {Component, Input, OnInit} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatDialog} from '@angular/material/dialog';
import {Router} from '@angular/router';
import {Study} from '@models/study';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {RegisterDialogComponent} from '../register-dialog/register-dialog.component';

@Component({
  standalone: true,
  selector: 'app-study-survey-entry',
  templateUrl: './study-survey-entry.component.html',
  styleUrls: ['./study-survey-entry.component.scss'],
  imports: [FlexModule, NgIf, MatButtonModule],
})
export class StudySurveyEntryComponent implements OnInit {
  @Input() study: Study;
  @Input() currentUser;
  @Input() surveyLink: string;

  constructor(
    private api: ApiService,
    private router: Router,
    private googleAnalytics: GoogleAnalyticsService,
    private authenticationService: AuthenticationService,
    public dialog: MatDialog,
  ) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
  }

  ngOnInit() {
    if (this.currentUser) {
      this.api.getUser(this.currentUser.id).subscribe(u => {
        this.currentUser = new User(u);
      });
    }
  }

  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  goSurvey() {
    if (this.surveyLink) {
      this.sendInquiry();
      this.googleAnalytics.studySurveyEvent(this.study);
      window.open(this.surveyLink, '_blank');
    }
  }

  sendInquiry() {
    this.api.sendStudyInquiryEmail(this.currentUser, this.study).subscribe();
    this.googleAnalytics.studyInquiryEvent(this.study);
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(RegisterDialogComponent, {
      width: `${window.innerWidth}px`,
      data: {
        displaySurvey: false,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.currentUser = true;
        this.goSurvey();
      }
    });
  }
}
