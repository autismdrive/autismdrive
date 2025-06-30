import {AsyncPipe, CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect, EventEmitter} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {ActivatedRoute, Router, RouterModule} from '@angular/router';
import {LoadingComponent} from '@app/loading/loading.component';
import {LogoComponent} from '@app/logo/logo.component';
import {scrollToTop} from '@app/shared/utilities/scrollToTop';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {FormlyMatInputModule} from '@ngx-formly/material/input';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {DeviceDetectorService} from 'ngx-device-detector';

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [
    AsyncPipe,
    CommonModule,
    FlexModule,
    FormlyMatInputModule,
    FormlyModule,
    LoadingComponent,
    LogoComponent,
    MatButtonModule,
    ReactiveFormsModule,
    RouterModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
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
        this.returnUrl = qParams['returnUrl'];
      }
    });

    this.route.params.subscribe(params => {
      if (params.hasOwnProperty('email_token')) {
        this.emailToken = params['email_token'];
      }
    });

    effect(() => {
      const user = this.authenticationService.currentUser();

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
