import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {ParticipantRelationship} from '../_models/participantRelationship';
import {Study} from '../_models/study';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-study-inquiry',
  templateUrl: './study-inquiry.component.html',
  styleUrls: ['./study-inquiry.component.scss']
})
export class StudyInquiryComponent implements OnInit {

  currentUser: User;
  @Input() study: Study;
  haveUserContact = false;
  inquirySent = false;
  alreadyInquired = false;

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private router: Router,
    private googleAnalytics: GoogleAnalyticsService
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  ngOnInit() {
    this.refreshUserAndInquiries();
  }

  refreshUserAndInquiries() {
    if (this.currentUser) {
      this.api.getUser(this.currentUser.id).subscribe(u => {
        const newU = new User(u);
        this.currentUser = newU;
        this.haveUserContact = newU.checkContact();
      });
      this.api.getUserStudyInquiries(this.currentUser.id).subscribe(userStudyInquiries => {
        userStudyInquiries.forEach(studyUser => {
          if (studyUser.study_id === this.study.id) {
            this.alreadyInquired = true;
          }
        });
      });
    }
  }


  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  goRegister() {
    this.router.navigateByUrl('/register');
  }

  sendInquiry() {
    this.api.sendStudyInquiryEmail(this.currentUser, this.study).subscribe();
    this.googleAnalytics.studyInquiryEvent(this.study);
    this.inquirySent = true;
  }

  goEditEnroll($event, participant) {
    if (participant.relationship === ParticipantRelationship.SELF_PARTICIPANT) {
      $event.preventDefault();
      this.router.navigate(['flow', 'self_intake', participant.id]);
    } else if (participant.relationship === ParticipantRelationship.DEPENDENT) {
      $event.preventDefault();
      this.router.navigate(['flow', 'dependent_intake', participant.id]);
    } else if (participant.relationship === ParticipantRelationship.SELF_PROFESSIONAL) {
      $event.preventDefault();
      this.router.navigate(['flow', 'professional_intake', participant.id]);
    } else if (participant.relationship === ParticipantRelationship.SELF_GUARDIAN) {
      $event.preventDefault();
      this.router.navigate(['flow', 'guardian_intake', participant.id]);
    }
  }

  goEligibility() {
    if (this.study && this.study.eligibility_url) {
      window.open(this.study.eligibility_url + '?user_id=' + this.currentUser.id, '_blank');
      this.sendInquiry();
    }
  }
}
