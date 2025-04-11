import {NgIf} from '@angular/common';
import {ChangeDetectorRef, Component} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {Router} from '@angular/router';
import {LoadingComponent} from '@app/loading/loading.component';
import {LogoComponent} from '@app/logo/logo.component';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';

@Component({
  standalone: true,
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
  imports: [FlexModule, LogoComponent, ReactiveFormsModule, FormlyModule, MatButtonModule, LoadingComponent, NgIf],
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
      this.api.sendResetPasswordEmail(this.model['email']).subscribe({
        next: token_url => {
          if (token_url) {
            localStorage.setItem('token_url', token_url);
          }
          this.formStatus = 'complete';
        },
        error: error1 => {
          if (error1) {
            this.errorMessage = error1;
          } else {
            this.errorMessage = 'We encountered an error resetting your password.  Please contact support.';
          }
          this.formStatus = 'form';
          this.changeDetectorRef.detectChanges();
        },
      });
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
