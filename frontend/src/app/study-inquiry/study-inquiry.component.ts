import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { AuthenticationService } from '../_services/api/authentication-service';
import { Router } from '@angular/router';
import { Study } from '../_models/study';
import { User } from '../_models/user';

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

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private router: Router
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    if (this.currentUser) {
      this.haveUserContact = this.currentUser.checkContact();
    }
  }

  ngOnInit() {
  }


  goLogin($event: MouseEvent) {
    $event.preventDefault();
    if (this.study) {
      this.router.navigateByUrl('/login');
    }
  }

  goRegister($event: MouseEvent) {
    $event.preventDefault();
    if (this.study) {
      this.router.navigateByUrl('/register');
    }
  }

  goProfile($event: MouseEvent) {
    $event.preventDefault();
    if (this.study) {
      this.router.navigateByUrl('/profile');
    }
  }

  sendInquiry() {
    this.api.sendStudyInquiryEmail(this.currentUser, this.study).subscribe();
    this.inquirySent = true;
  }

}
