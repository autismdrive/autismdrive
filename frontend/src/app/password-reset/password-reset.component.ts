import {ChangeDetectorRef, Component} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {scrollToTop} from '@util/scrollToTop';
import {DeviceDetectorService} from 'ngx-device-detector';
import {PasswordRequirements} from '@models/password_requirements';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent {
  token: string;
  formState = 'form';
  errorMessage = '';
  form = new FormGroup({});
  model: any = {};
  role: string;
  passwordRequirements: PasswordRequirements;
  passwordRegex: RegExp;
  fields: FormlyFieldConfig[] = [
    {
      key: 'password',
      validators: {
        fieldMatch: {
          expression: control => {
            const value = control.value;

            // avoid displaying the message error when values are empty
            return value.passwordConfirm === value.password || !value.passwordConfirm || !value.password;
          },
          message: 'Password Not Matching',
          errorPath: 'passwordConfirm',
        },
      },
      fieldGroup: [
        {
          key: 'password',
          type: 'input',
          className: 'password',
          props: {
            type: 'password',
            label: 'Password',
            required: true,
          },
          validators: {
            password: {
              expression: c => !c.value || this.passwordRegex.test(c.value),
              message: (error, field: FormlyFieldConfig) => this.passwordRequirements.instructions,
            },
          },
        },
        {
          key: 'passwordConfirm',
          type: 'input',
          className: 'passwordConfirm',
          props: {
            type: 'password',
            label: 'Confirm Password',
            placeholder: 'Please re-enter your password',
            required: true,
          },
        },
      ],
    },
  ];

  constructor(
    private authenticationService: AuthenticationService,
    private route: ActivatedRoute,
    private router: Router,
    private changeDetectorRef: ChangeDetectorRef,
    private apiService: ApiService,
    private deviceDetectorService: DeviceDetectorService,
    private googleAnalyticsService: GoogleAnalyticsService,
  ) {
    this.route.params.subscribe(params => {
      this.token = params['email_token'];
      this.role = params['role'];
      this.apiService.getPasswordRequirements(this.role).subscribe(reqs => {
        this.passwordRequirements = reqs;
        this.passwordRegex = RegExp(reqs.regex);
      });
    });
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  submit() {
    if (this.form.valid) {
      this.formState = 'submitting';
      this.errorMessage = '';

      this.authenticationService.resetPassword(this.model['password']['password'], this.token).subscribe(
        data => {
          this._goToReturnUrl(data);
          this.googleAnalyticsService.accountEvent('reset_password');
        },
        error1 => {
          if (error1.code === 'token_expired') {
            this.errorMessage =
              'The link for resetting your password has expired.' +
              'Please return to the password reset page to generate a new email.';
          } else {
            this.errorMessage = 'We encountered an error resetting your password.  Please contact support.';
          }
          this.formState = 'form';
          this.changeDetectorRef.detectChanges();
        },
      );
    }
  }

  updateValidationState() {
    this.form.updateValueAndValidity();
  }

  private _goToReturnUrl(user: User) {
    const storedUrl = localStorage.getItem('returnUrl');
    const returnUrl = storedUrl && storedUrl !== 'undefined' ? storedUrl : '/profile';
    if (user) {
      this.router.navigateByUrl(returnUrl).then(_ => scrollToTop(this.deviceDetectorService));
    }
  }
}
