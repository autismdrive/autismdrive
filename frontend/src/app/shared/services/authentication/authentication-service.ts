import {HttpClient} from '@angular/common/http';
import {effect, Injectable, signal, WritableSignal} from '@angular/core';
import {ApiError} from '@app/api-error';
import {User} from '@app/shared/models/user';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';
import {AuthenticationStateService} from '@app/shared/services/authentication/authentication-state-service';
import {Observable, throwError} from 'rxjs';
import {catchError, finalize, map} from 'rxjs/operators';
import {GoogleAnalyticsService} from '../google-analytics/google-analytics.service';

@Injectable({providedIn: 'root'})
export class AuthenticationService {
  public currentUser: WritableSignal<User | undefined> = signal(undefined);
  urls = {
    login: null,
    resetPassword: null,
    refresh: null,
  };
  public status: WritableSignal<'loading' | 'loaded' | 'error' | 'idle'> = signal('idle');

  constructor(
    private http: HttpClient,
    private appEnvironmentService: AppEnvironmentService,
    private authStateService: AuthenticationStateService,
    private googleAnalyticsService: GoogleAnalyticsService,
  ) {
    this.status.set('loading');
    effect(() => {
      if (this.appEnvironmentService.props()) {
        const token = this.authStateService.authToken;
        const apiUrl = this.appEnvironmentService?.apiUrl;

        this.urls = {
          login: `${apiUrl}/api/login_password`,
          resetPassword: `${apiUrl}/api/reset_password`,
          refresh: `${apiUrl}/api/session`,
        };

        if (token) {
          this.refresh().subscribe(); // Make sure the api still considers the in-memory user as valid.
        } else {
          this.status.set('loaded');
          this.currentUser.set(undefined);
        }
      }
    });
  }

  isLoggedIn(): boolean {
    return !!this.authStateService.authToken && !!this.currentUser();
  }

  private _handleError(error: ApiError) {
    let message = 'Could not complete your request; please try again later.';
    message = error.message;

    this.googleAnalyticsService?.errorEvent(error);

    // return an observable with a user-facing error message
    return throwError(() => message);
  }

  private loadUser(userDict): User {
    // login successful if there's a jwt token in the response
    const user = new User(userDict);
    this.currentUser.set(user);
    this.authStateService.setUser(user);
    return user;
  }

  login(email: string, password: string, email_token = ''): Observable<User> {
    const body = {email, password, email_token};
    return this.http.post<any>(this.urls.login, body).pipe(
      map(userDict => this.loadUser(userDict)),
      catchError(this._handleError.bind(this)),
    );
  }

  private refresh(): Observable<User> {
    // For a refresh, we'll hold to the existing token, and try to make the request.
    return this.http.get<any>(this.urls.refresh).pipe(
      map(userDict => {
        return this.loadUser(userDict);
      }),
      catchError((_err, _caught) => {
        this.authStateService.removeUser();
        this.currentUser.set(undefined);

        // return an observable with a user-facing error message
        return throwError(() => 'Could not refresh session; please log in again.');
      }),
      finalize(() => {
        this.status.set('loaded');
      }),
    );
  }

  resetPassword(newPassword: string, email_token: string): Observable<any> {
    const reset = {password: newPassword, email_token: email_token};
    return this.http.post<any>(this.urls.resetPassword, reset).pipe(
      map(userDict => {
        return this.loadUser(userDict);
      }),
    );
  }

  logout() {
    // remove user from local storage to log user out
    this.authStateService.removeUser();
    this.currentUser.set(undefined);
  }
}
