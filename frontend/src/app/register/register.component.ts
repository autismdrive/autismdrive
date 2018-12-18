import { ChangeDetectorRef, Component, EventEmitter, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService}  from '../api.service';
import { User } from '../user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  user: User;
  errorEmitter = new EventEmitter<string>();
  registerState = 'form';
  errorMessage = '';
  form = new FormGroup({});
  model: any = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'first_name',
      type: 'input',
      templateOptions: {
        label: 'First Name:',
        placeholder: 'Enter your first name',
        required: true,
      },
    },
    {
      key: 'last_name',
      type: 'input',
      templateOptions: {
        label: 'Last Name:',
        placeholder: 'Enter your last name',
        required: true,
      },
    },
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
    this.user = {id:null, first_name:this.model['first_name'], last_name:this.model['last_name'], email:this.model['email'], role:'User'}
  }

  ngOnInit() {
  }

  submit() {
    if (this.form.valid) {
      this.registerState = 'submitting';
      this.errorMessage = '';
      console.log('Register state is submitting');

      this.user['first_name'] = this.model['first_name'];
      this.user['last_name'] = this.model['last_name'];
      this.user['email'] = this.model['email'];

      this.api.addUser(this.user).subscribe(u => {
        this.user = u;
        this.registerState = 'wait_for_email';
        this.changeDetectorRef.detectChanges();
        console.log('Register state is wait_for_email');
      }, error1 => {
        this.registerState = 'form';
        this.errorMessage = error1;
        this.changeDetectorRef.detectChanges();
        console.log('Register state is form?' + this.registerState);
      });
    }
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }
}
