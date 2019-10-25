import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';
import {PasswordRequirements} from '../_models/password_requirements';
import {GoogleAnalyticsService} from '../google-analytics.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss']
})
export class PasswordResetComponent implements OnInit {

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
          expression: (control) => {
            const value = control.value;

            // avoid displaying the message error when values are empty
            return value.passwordConfirm === value.password  || (!value.passwordConfirm || !value.password);
          },
          message: 'Password Not Matching',
          errorPath: 'passwordConfirm',
        },
      },
      fieldGroup: [
        {
          key: 'password',
          type: 'input',
          templateOptions: {
            type: 'password',
            label: 'Password',
            required: true,
          },
          validators: {
            password: {
              expression: (c) => !c.value || this.passwordRegex.test(c.value),
              message: (error, field: FormlyFieldConfig) => this.passwordRequirements.instructions,
            }
          }
        },
        {
          key: 'passwordConfirm',
          type: 'input',
          templateOptions: {
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
    private googleAnalyticsService: GoogleAnalyticsService
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

  ngOnInit() {
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
          this.router.navigate(['profile']);
          this.googleAnalyticsService.accountEvent('reset_password');
        }, error1 => {
          this.formState = 'form';
          this.errorMessage = error1;
          this.changeDetectorRef.detectChanges();
        });
    }
  }

  updateValidationState() {
    this.form.updateValueAndValidity();
  }
}
