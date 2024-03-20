import {ChangeDetectorRef, Component, Inject, OnInit} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {ActivatedRoute} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {StudySurveyEntryComponent} from '../study-survey-entry/study-survey-entry.component';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-register-dialog',
  templateUrl: './register-dialog.component.html',
  styleUrls: ['./register-dialog.component.scss'],
})
export class RegisterDialogComponent implements OnInit {
  private _stateSubject: BehaviorSubject<string>;
  public registerState: Observable<string>;

  user: User;
  errorMessage = '';
  form = new FormGroup({});
  model: any = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'email',
      validators: {
        fieldMatch: {
          expression: control => {
            const value = control.value;

            // avoid displaying the message error when values are empty
            return value.emailConfirm === value.email || !value.emailConfirm || !value.email;
          },
          message: 'Email Does Not Match',
          errorPath: 'emailConfirm',
        },
      },
      fieldGroup: [
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
          },
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
        },
      ],
    },
  ];

  constructor(
    private api: ApiService,
    private changeDetectorRef: ChangeDetectorRef,
    private route: ActivatedRoute,
    private googleAnalytics: GoogleAnalyticsService,
    public dialogRef: MatDialogRef<StudySurveyEntryComponent>,
    @Inject(MAT_DIALOG_DATA)
    public data: {
      displaySurvey: boolean;
    },
  ) {
    this._stateSubject = new BehaviorSubject<string>('form');
    this.registerState = this._stateSubject.asObservable();

    // Create an empty user instance to hold the form data.
    this.user = new User({
      id: null,
      email: this.model['email'],
      role: 'User',
    });
  }

  ngOnInit() {}

  submit() {
    localStorage.removeItem('token_url');
    if (this.form.valid) {
      this._stateSubject.next('submitting');
      this.registerState = this._stateSubject.asObservable();
      this.errorMessage = '';

      // Add email address from the form into the user instance.
      this.user['email'] = this.model['email']['email'];

      // Submit the user data to the backend.
      this.api.addUser(this.user).subscribe(
        u => {
          this.user = u;
          if (u.hasOwnProperty('token_url')) {
            localStorage.setItem('token_url', u.token_url);
          }
          this.googleAnalytics.accountEvent('register');
          this._stateSubject.next('wait_for_email');
          this.registerState = this._stateSubject.asObservable();
          this.changeDetectorRef.detectChanges();
          this.data.displaySurvey = true;
        },
        error1 => {
          this._stateSubject.next('form');
          this.registerState = this._stateSubject.asObservable();
          this.errorMessage = error1;
          this.changeDetectorRef.detectChanges();
        },
      );
    }
  }

  public get registerStateValue(): string {
    return this._stateSubject.value;
  }
}
