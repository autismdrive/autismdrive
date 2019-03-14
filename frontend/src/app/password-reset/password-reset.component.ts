import { ChangeDetectorRef, Component, EventEmitter, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Router} from '@angular/router';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../_services/api/api.service';

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
  fields: FormlyFieldConfig[] = [
    {
      key: 'password',
      validators: {
      fieldMatch: {
        expression: (control) => {
          const value = control.value;

          return value.passwordConfirm === value.password
            // avoid displaying the message error when values are empty
            || (!value.passwordConfirm || !value.password);
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
          placeholder: 'Must be at least 3 characters',
          required: true,
          minLength: 3,
        },
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
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private changeDetectorRef: ChangeDetectorRef
  ) {this.route.params.subscribe(params => {
      this.token = params['email_token'];
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

      this.api.resetPassword(this.model['password']['password'], this.token).subscribe(auth_token => {
          this.formState = 'complete';
          this.changeDetectorRef.detectChanges();
          this.api.openSession(auth_token['token']).subscribe(session => {
              this.router.navigate(['profile']);
          });
        }, error1 => {
          this.formState = 'form';
          this.errorMessage = error1;
          this.changeDetectorRef.detectChanges();
        });
    }
  }


}
