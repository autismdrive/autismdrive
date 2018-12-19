import { Component, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  emailToken: string;
  errorEmitter = new EventEmitter<string>();
  form = new FormGroup({});
  model: any = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'email',
      type: 'input',
      templateOptions: {
        type: 'email',
        label: 'Email Address:',
        placeholder: 'Enter email',
        required: true,
      },
    },
    {
      key: 'password',
      type: 'input',
      templateOptions: {
        label: 'Password:',
        type: 'password',
        required: true,
      },
    },
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private api: ApiService
  ) {
    this.route.params.subscribe(params => {
      if ('email_token' in params) {
        this.emailToken = params['email_token'];
      }
    });
  }

  ngOnInit() {
  }

  submit() {
    if (this.form.valid) {
      this.api.login(this.model['email'], this.model['password'], this.emailToken).subscribe(
        token => {
          this.api.openSession(token['token']).subscribe(
            user => {
              this.router.navigate(['profile']);
            }
          )
        }, error1 => {
          if (error1) {
            this.errorEmitter.emit(error1);
          } else {
            this.errorEmitter.emit('An unexpected error occurred. Please contact support')
          }
        }
      );
    }
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  goTerms($event) {
    $event.preventDefault();
    this.router.navigate(['terms']);
  }

  goForgotPassword($event) {
    $event.preventDefault();
    this.router.navigate(['forgot-password']);
  }
}
