import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-study-survey-entry',
  templateUrl: './study-survey-entry.component.html',
  styleUrls: ['./study-survey-entry.component.scss']
})
export class StudySurveyEntryComponent implements OnInit {
  @Input() currentUser = false;
  @Input() surveyLink: string;

  constructor(
    private router: Router,
  ) { }

  ngOnInit() {
  }

  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  goRegister() {
    this.router.navigateByUrl('/register');
  }

  goSurvey() {
    if (this.surveyLink) {
      window.open(this.surveyLink, '_blank');
    }
  }
}
