import { ChangeDetectorRef, Component, EventEmitter, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  user: User;
  registerState = 'form';
  errorMessage = '';
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
  ) {
    this.user = new User(null, this.model['email'], 'User');
  }

  ngOnInit() {
  }

  submit() {
    if (this.form.valid) {
      this.registerState = 'submitting';
      this.errorMessage = '';
      this.user['email'] = this.model['email'];

      this.api.addUser(this.user).subscribe(u => {
        this.user = u;
        this.registerState = 'wait_for_email';
        this.changeDetectorRef.detectChanges();
      }, error1 => {
        this.registerState = 'form';
        this.errorMessage = error1;
        this.changeDetectorRef.detectChanges();
      });
    }
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }
}
