import {ChangeDetectorRef, Component} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {GoogleAnalyticsService} from '../_services/google-analytics/google-analytics.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  private _stateSubject: BehaviorSubject<string>;
  public registerState: Observable<string>;

  user: User;
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
      validators: {
        validation: ['email'],
      },
    },
  ];
  constructor(
    private api: ApiService,
    private changeDetectorRef: ChangeDetectorRef,
    private router: Router,
    private route: ActivatedRoute,
    private googleAnalytics: GoogleAnalyticsService,
    private meta: Meta,
  ) {
    this._stateSubject = new BehaviorSubject<string>('form');
    this.registerState = this._stateSubject.asObservable();
    this.user = new User({
      id: null,
      email: this.model['email'],
      role: 'User',
    });
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/assets/join/hero.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/assets/join/hero.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/assets/join/hero.jpg'},
      `name='twitter:image'`,
    );
  }

  submit() {
    localStorage.removeItem('token_url');
    localStorage.setItem('returnUrl', this.route.snapshot.queryParams['returnUrl']);
    if (this.form.valid) {
      this._stateSubject.next('submitting');
      this.registerState = this._stateSubject.asObservable();
      this.errorMessage = '';
      this.user['email'] = this.model['email'];

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

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  public get registerStateValue(): string {
    return this._stateSubject.value;
  }
}
