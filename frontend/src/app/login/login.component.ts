import { Component, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loading = false;
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
    private authenticationService: AuthenticationService
  ) {
    this.route.params.subscribe(params => {
      if ('email_token' in params) {
        this.emailToken = params['email_token'];
      }
    });
  }

  ngOnInit() {
  }

  submit(model) {
    this.loading = true;

    if (this.form.valid) {
      this.authenticationService.login(model['email'], model['password'], this.emailToken).subscribe(
          data => {
            this.router.navigate(['profile']);
          },
          error => {
            if (error) {
              this.errorEmitter.emit(error);
            } else {
              this.errorEmitter.emit('An unexpected error occurred. Please contact support');
            }
            this.loading = false;
          });
    } else {
      this.loading = false;
      this.errorEmitter.emit('Please enter a valid email address and password.');
    }
  }

}
