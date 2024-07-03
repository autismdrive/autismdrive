import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable, throwError} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {StarError} from '../../star-error';
import {User} from '../../_models/user';
import {ConfigService} from '../config/config.service';
import {GoogleAnalyticsService} from '../google-analytics/google-analytics.service';

@Injectable({providedIn: 'root'})
export class AuthenticationService {
  public static LOCAL_TOKEN_KEY = 'star_token';
  private currentUserSubject = new BehaviorSubject<User>(null);
  public currentUser: Observable<User>;

  private login_url: string;
  private reset_pass_url: string;
  private refresh_url: string;

  constructor(
    private http: HttpClient,
    private googleAnalyticsService: GoogleAnalyticsService,
    private configService: ConfigService,
  ) {
    const token = localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY);
    this.login_url = `${configService.apiUrl}/api/login_password`;
    this.reset_pass_url = `${configService.apiUrl}/api/reset_password`;
    this.refresh_url = `${configService.apiUrl}/api/session`;

    this.currentUser = this.currentUserSubject.asObservable();
    if (token) {
      this._refresh().subscribe(); // Make sure the api still considers the in-memory user as valid.
    } else {
      this.currentUserSubject.next(null);
    }
  }

  private _handleError(error: StarError) {
    let message = 'Could not complete your request; please try again later.';
    message = error.message;
    // return an observable with a user-facing error message
    return throwError(message);
  }

  private loadUser(userDict): User {
    // login successful if there's a jwt token in the response
    if (userDict.token) {
      localStorage.setItem(AuthenticationService.LOCAL_TOKEN_KEY, userDict.token);
    }
    const user = new User(userDict);
    this.currentUserSubject.next(user);
    console.log('The current user subject is now set.', user);
    this.googleAnalyticsService.set_user(user.id);
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
          this.currentUserSubject.next(null);
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
    localStorage.removeItem(AuthenticationService.LOCAL_TOKEN_KEY);
    this.currentUserSubject.next(null);
    this.googleAnalyticsService.set_user(null);
  }
}
