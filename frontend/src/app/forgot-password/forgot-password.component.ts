import { ChangeDetectorRef, Component, EventEmitter, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../_services/api/api.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {
  errorMessage: string;
  formStatus = 'form';
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
  ];
  constructor(
    private api: ApiService,
    private changeDetectorRef: ChangeDetectorRef,
    private router: Router
  ) { }

  ngOnInit() {
  }

  submit() {
    if (this.form.valid) {
      this.formStatus = 'submitting';
      this.api.sendResetPasswordEmail(this.model['email']).subscribe(e => {
        this.formStatus = 'complete';
      }, error1 => {
        if (error1) {
          this.errorMessage = error1;
        } else {
          this.errorMessage = 'We encountered an error resetting your password.  Please contact support.';
        }
        this.formStatus = 'form';
        this.changeDetectorRef.detectChanges();
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
