import {Component, EventEmitter} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {scrollToTop} from '@util/scrollToTop';
import {DeviceDetectorService} from 'ngx-device-detector';
import {User} from '@models/user';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loading = false;
  emailToken: string;
  errorEmitter = new EventEmitter<string>();
  form = new FormGroup({});
  model: any = {};
  returnUrl: string;
  fields: FormlyFieldConfig[] = [
    {
      key: 'email',
      type: 'input',
      props: {
        type: 'email',
        label: 'Email Address:',
        placeholder: 'Enter email',
        required: true,
      },
    },
    {
      key: 'password',
      type: 'input',
      props: {
        label: 'Password:',
        type: 'password',
        required: true,
      },
    },
  ];

  constructor(
    private authenticationService: AuthenticationService,
    private deviceDetectorService: DeviceDetectorService,
    private googleAnalytics: GoogleAnalyticsService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.route.queryParams.subscribe(qParams => {
      if (qParams.hasOwnProperty('returnUrl')) {
        this.returnUrl = qParams.returnUrl;
        this.authenticationService.currentUser.subscribe(u => this._goToReturnUrl(u));
      }
    });

    this.route.params.subscribe(params => {
      if (params.hasOwnProperty('email_token')) {
        this.emailToken = params.email_token;
      }
    });
    this.authenticationService.currentUser.subscribe(user => {
      // If the login form discovers there is a user, send folks to the return url.
      if (user) {
        this._goToReturnUrl(user);
      }
    });
  }

  submit(model) {
    this.loading = true;

    if (this.form.valid) {
      this.authenticationService.login(model['email'], model['password'], this.emailToken).subscribe(
        u => {
          this._goToReturnUrl(u);
          this.googleAnalytics.accountEvent('login');
        },
        error => {
          if (error) {
            this.errorEmitter.emit(error);
          } else {
            this.errorEmitter.emit('An unexpected error occurred. Please contact support');
          }
          this.loading = false;
        },
      );
    } else {
      this.loading = false;
      this.errorEmitter.emit('Please enter a valid email address and password.');
    }
  }

  private _goToReturnUrl(user: User) {
    if (user) {
      this.router.navigateByUrl(this.returnUrl || '/profile').then(_ => scrollToTop(this.deviceDetectorService));
    }
  }
}
