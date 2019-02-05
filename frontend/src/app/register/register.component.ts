import { ChangeDetectorRef, Component, EventEmitter, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { FormlyFieldConfig } from '@ngx-formly/core';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { Participant } from '../participant';

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
    this.user = {
      id: null,
      email: this.model['email'],
      role: 'User',
      participants: [
        {
          id: null,
          user_id: null,
          participant_id: null,
          relationship: 'self',
          participant: new Participant({
            id: null,
            first_name: this.model['first_name'],
            last_name: this.model['last_name'],
          })
        }
      ]
    };
  }

  ngOnInit() {
  }

  submit() {
    if (this.form.valid) {
      this.registerState = 'submitting';
      this.errorMessage = '';
      this.user['first_name'] = this.model['first_name'];
      this.user['last_name'] = this.model['last_name'];
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
