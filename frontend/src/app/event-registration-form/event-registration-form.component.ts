import {ChangeDetectorRef, Component, Inject, OnInit} from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../_models/user';
import {FormGroup} from '@angular/forms';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {ApiService} from '../_services/api/api.service';
import {ActivatedRoute} from '@angular/router';
import {GoogleAnalyticsService} from '../google-analytics.service';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {EventRegistrationComponent} from '../event-registration/event-registration.component';

@Component({
  selector: 'app-event-registration-form',
  templateUrl: './event-registration-form.component.html',
  styleUrls: ['./event-registration-form.component.scss']
})
export class EventRegistrationFormComponent implements OnInit {
  private _stateSubject: BehaviorSubject<string>;
  public registerState: Observable<string>;

  user: User;
  errorMessage = '';
  form = new FormGroup({});
  model: any = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'first_name',
      type: 'input',
      templateOptions: {
        label: 'First Name:',
        required: true,
      },
    },
    {
      key: 'last_name',
      type: 'input',
      templateOptions: {
        label: 'Last Name:',
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
      validators: {
        validation: ['email'],
      }
    },
    {
      key: 'emailConfirm',
      type: 'input',
      templateOptions: {
        type: 'email',
        label: 'Confirm Email',
        placeholder: 'Please re-enter your email',
        required: true,
      },
      validators: {
        validation: ['emailConfirm'],
      }
    },
    {
      key: 'zipcode',
      type: 'input',
      templateOptions: {
        type: 'number',
        label: 'Zip Code:',
        max: 99999,
        min: 0,
        pattern: '\\d{5}',
        required: true,
      },
    },
    {
      key: 'relationship_to_autism',
      type: 'multicheckbox',
      templateOptions: {
        label: 'Relationship to Autism:',
        description: '(select all that apply)',
        type: 'array',
        options: [
          {'value': 'friend_colleague', 'label': 'Friend/Colleague'},
          {'value': 'family_member', 'label': 'Parent/Family Member'},
          {'value': 'self_advocate', 'label': 'Individual With Autism'},
          {'value': 'professional', 'label': 'Professional'},
          {'value': 'other', 'label': 'Other'},
        ],
        required: true,
      },
    },
    {
      key: 'relationship_other',
      type: 'input',
      templateOptions: {
        label: 'How else are you related to Autism',
      },
      hideExpression: '!(model.relationship_to_autism && model.relationship_to_autism.includes("other"))',
    },
    {
      key: 'marketing_channel',
      type: 'multicheckbox',
      templateOptions: {
        label: 'How did you find about the virtual event?:',
        description: '(select all that apply)',
        type: 'array',
        options: [
          {'value': 'star_newsletter', 'label': 'STAR e-newsletter'},
          {'value': 'facebook', 'label': 'Facebook'},
          {'value': 'drive', 'label': 'Autism DRIVE'},
          {'value': 'family_member', 'label': 'Parent/Family Member'},
          {'value': 'friend_colleague', 'label': 'Friend/Colleague'},
          {'value': 'other', 'label': 'Other'},
        ],
        required: true,
      },
    },
    {
      key: 'marketing_other',
      type: 'input',
      templateOptions: {
        label: 'What other ways did you find out about this event',
      },
      hideExpression: '!(model.marketing_channel && model.marketing_channel.includes("other"))',
    },
    {
      key: 'newsletter_signup',
      type: 'checkbox',
      defaultValue: true,
      templateOptions: {
        label: 'Please sign me up for the STAR E-newsletter',
        description: 'Send me notifications of workshops, information, events, and research opportunities offered ' +
          'by the UVA Supporting Transformative Autism Research Initiative and partnering organizations.',
      },
    },
  ];

  constructor(
    private api: ApiService,
    private changeDetectorRef: ChangeDetectorRef,
    private route: ActivatedRoute,
    private googleAnalytics: GoogleAnalyticsService,
    public dialogRef: MatDialogRef<EventRegistrationComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      registered: boolean
    }
  ) {
    this._stateSubject = new BehaviorSubject<string>('form');
    this.registerState = this._stateSubject.asObservable();
    this.user = new User({
      id: null,
      email: this.model['email'],
      role: 'User'
    });
  }

  ngOnInit() {
  }

  submit() {
    localStorage.removeItem('token_url');
    if (this.form.valid) {
      this._stateSubject.next('submitting');
      this.registerState = this._stateSubject.asObservable();
      this.errorMessage = '';
      this.user['email'] = this.model['email']['email'];

      this.api.addUser(this.user).subscribe(u => {
        this.user = u;
        if (u.hasOwnProperty('token_url')) {
          localStorage.setItem('token_url', u.token_url);
        }
        this.googleAnalytics.accountEvent('register');
        this._stateSubject.next('wait_for_email');
        this.registerState = this._stateSubject.asObservable();
        this.changeDetectorRef.detectChanges();
        this.data.registered = true;
      }, error1 => {
        this._stateSubject.next('form');
        this.registerState = this._stateSubject.asObservable();
        this.errorMessage = error1;
        this.changeDetectorRef.detectChanges();
      });
    }
  }

  public get registerStateValue(): string {
    return this._stateSubject.value;
  }

}
