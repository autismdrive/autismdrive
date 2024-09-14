import {ChangeDetectorRef, Component} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent {
  errorMessage: string;
  formStatus = 'form';
  form = new FormGroup({});
  model: any = {};
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
  ];
  constructor(
    private api: ApiService,
    private changeDetectorRef: ChangeDetectorRef,
    private router: Router,
  ) {}

  submit() {
    localStorage.removeItem('token_url');
    if (this.form.valid) {
      this.formStatus = 'submitting';
      this.api.sendResetPasswordEmail(this.model['email']).subscribe(
        token_url => {
          if (token_url) {
            localStorage.setItem('token_url', token_url);
          }
          this.formStatus = 'complete';
        },
        error1 => {
          if (error1) {
            this.errorMessage = error1;
          } else {
            this.errorMessage = 'We encountered an error resetting your password.  Please contact support.';
          }
          this.formStatus = 'form';
          this.changeDetectorRef.detectChanges();
        },
      );
    }
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  goRegister($event) {
    $event.preventDefault();
    this.router.navigate(['register']);
  }
}
