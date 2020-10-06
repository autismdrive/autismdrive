import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {Study} from '../_models/study';
import {GoogleAnalyticsService} from '../google-analytics.service';
import {MatDialog} from '@angular/material/dialog';
import {RegisterDialogComponent} from '../register-dialog/register-dialog.component';

@Component({
  selector: 'app-study-survey-entry',
  templateUrl: './study-survey-entry.component.html',
  styleUrls: ['./study-survey-entry.component.scss']
})
export class StudySurveyEntryComponent implements OnInit {
  @Input() study: Study;
  @Input() currentUser = false;
  @Input() surveyLink: string;

  constructor(
    private router: Router,
    private googleAnalytics: GoogleAnalyticsService,
    public dialog: MatDialog
  ) { }

  ngOnInit() {
  }

  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  goSurvey() {
    if (this.surveyLink) {
      this.googleAnalytics.studySurveyEvent(this.study);
      window.open(this.surveyLink, '_blank');
    }
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(RegisterDialogComponent, {
      width: `${window.innerWidth}px`,
      data: {
        'displaySurvey': false
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.currentUser = true;
        this.goSurvey();
      }
    });
  }
}
