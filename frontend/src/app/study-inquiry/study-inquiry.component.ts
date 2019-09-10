import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { AuthenticationService } from '../_services/api/authentication-service';
import { Router } from '@angular/router';
import { Study } from '../_models/study';
import { User } from '../_models/user';
import { ParticipantRelationship } from '../_models/participantRelationship';

@Component({
  selector: 'app-study-inquiry',
  templateUrl: './study-inquiry.component.html',
  styleUrls: ['./study-inquiry.component.scss']
})
export class StudyInquiryComponent implements OnInit {

  currentUser: User;
  @Input() study: Study;
  haveUserContact:boolean = false;
  inquirySent: boolean = false;
  alreadyInquired: boolean = false;

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private router: Router
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    if (this.currentUser) {
      this.haveUserContact = this.currentUser.checkContact();
      this.api.getUserStudyInquiries(this.currentUser.id).subscribe(
        userStudyInquiries => {
          for ( let i in userStudyInquiries ) {
            if (this.study.id == userStudyInquiries[i].study_id) {
              this.alreadyInquired = true;
            }
          }
        }
      );
      for (let i in this.currentUser.participants) {
        this.api
          .getFlow(this.currentUser.participants[i].getFlowName(), this.currentUser.participants[i].id)
          .subscribe(f => {
            this.currentUser.participants[i].percent_complete = f.percentComplete();
          });
      }
    }
  }

  ngOnInit() {
  }


  goLogin() {
    this.router.navigate(['/login'], { queryParams: { returnUrl: this.router.url } });
  }

  goRegister() {
    this.router.navigateByUrl('/register');
  }

  goProfile() {
    this.router.navigateByUrl('/profile');
  }

  sendInquiry() {
    this.api.sendStudyInquiryEmail(this.currentUser, this.study).subscribe();
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
    } else {
      $event.preventDefault();
      this.router.navigate(['flow', 'guardian_intake', participant.id]);
    }
  }


}
