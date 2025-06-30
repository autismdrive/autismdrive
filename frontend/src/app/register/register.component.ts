import {CommonModule} from '@angular/common';
import {ChangeDetectorRef, Component} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, Router} from '@angular/router';
import {LoadingComponent} from '@app/loading/loading.component';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationStateService} from '@services/authentication/authentication-state-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {StorageService} from '@services/storage/storage.service';
import {BehaviorSubject, Observable} from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  imports: [FlexModule, ReactiveFormsModule, FormlyModule, MatButtonModule, LoadingComponent, CommonModule],
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
      props: {
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
    private storageService: StorageService,
  ) {
    this._stateSubject = new BehaviorSubject<string>('form');
    this.registerState = this._stateSubject.asObservable();
    this.user = new User({
      id: null,
      email: this.model['email'],
      role: 'User',
    });
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/public/join/hero.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/public/join/hero.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/public/join/hero.jpg'},
      `name='twitter:image'`,
    );
  }

  submit() {
    this.storageService.remove('token_url');
    this.storageService.set('returnUrl', this.route.snapshot.queryParams['returnUrl']);
    if (this.form.valid) {
      this._stateSubject.next('submitting');
      this.registerState = this._stateSubject.asObservable();
      this.errorMessage = '';
      this.user['email'] = this.model['email'];

      this.api.addUser(this.user).subscribe(
        u => {
          this.user = u;
          if (u.hasOwnProperty('token_url')) {
            this.storageService.set(AuthenticationStateService.LOCAL_TOKEN_URL_KEY, u.token_url);
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
