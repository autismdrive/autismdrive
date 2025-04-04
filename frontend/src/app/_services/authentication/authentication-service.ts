import {HttpClient} from '@angular/common/http';
import {effect, Injectable, signal, WritableSignal} from '@angular/core';
import {ApiError} from '@app/api-error';
import {User} from '@models/user';
import {AuthenticationStateService} from '@services/authentication/authentication-state-service';
import {ConfigService} from '@services/config/config.service';
import {Observable, throwError} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {GoogleAnalyticsService} from '../google-analytics/google-analytics.service';

@Injectable({providedIn: 'root'})
export class AuthenticationService {
  public currentUser: WritableSignal<User | undefined> = signal(undefined);

  private login_url: string;
  private reset_pass_url: string;
  private refresh_url: string;

  constructor(
    private http: HttpClient,
    private configService: ConfigService,
    private authStateService: AuthenticationStateService,
    private googleAnalyticsService: GoogleAnalyticsService,
  ) {
    console.log('AuthenticationService > constructor > configService.props()', this.configService.props());

    effect(() => {
      console.log('AuthenticationService > constructor > effect > configService.props()', this.configService.props());
      if (this.configService.props()) {
        const token = this.authStateService.authToken;
        this.login_url = `${this.configService?.apiUrl}/api/login_password`;
        this.reset_pass_url = `${this.configService?.apiUrl}/api/reset_password`;
        this.refresh_url = `${this.configService?.apiUrl}/api/session`;

        if (token) {
          this._refresh().subscribe(); // Make sure the api still considers the in-memory user as valid.
        } else {
          this.currentUser.set(undefined);
        }
      }
    });
  }

  private _handleError(error: ApiError) {
    let message = 'Could not complete your request; please try again later.';
    message = error.message;

    this.googleAnalyticsService.errorEvent(error);

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
    return this.http.post<any>(this.login_url, body).pipe(
      map(userDict => this.loadUser(userDict)),
      catchError(this._handleError),
    );
  }

  private _refresh(): Observable<User> {
    // For a refresh, we'll hold to the existing token, and try to make the request.
    return this.http.get<any>(this.refresh_url).pipe(
      map(
        userDict => {
          return this.loadUser(userDict);
        },
        error => {
          this.currentUser.set(undefined);
          this.authStateService.currentUser.set(undefined);
        },
      ),
    );
  }

  refresh() {
    this._refresh().subscribe();
  }

  resetPassword(newPassword: string, email_token: string): Observable<any> {
    const reset = {password: newPassword, email_token: email_token};
    return this.http.post<any>(this.reset_pass_url, reset).pipe(
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
