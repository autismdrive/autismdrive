import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {BehaviorSubject, Observable, ObservableInput, of, throwError} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {User} from '../../_models/user';
import {environment} from '../../../environments/environment';
import {GoogleAnalyticsService} from '../../google-analytics.service';


@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  public static LOCAL_TOKEN_KEY = 'star_token';

  private token: String;
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser: Observable<User>;
  login_url = `${environment.api}/api/login_password`;
  reset_pass_url = `${environment.api}/api/reset_password`;
  refresh_url = `${environment.api}/api/session`;


  constructor(private http: HttpClient, private googleAnalyticsService: GoogleAnalyticsService) {
    this.token = localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY);
    this.currentUserSubject = new BehaviorSubject<User>(null);
    this.currentUser = this.currentUserSubject.asObservable();
    if (this.token) {
      this.refresh().subscribe();  // Make sure the api still considers the in-memory user as valid.
    }
  }


  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  private loadUser(userDict): User {
    // login successful if there's a jwt token in the response
    if (userDict && userDict.token) {
      const user = new User(userDict);
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      localStorage.setItem(AuthenticationService.LOCAL_TOKEN_KEY, user.token);
      this.currentUserSubject.next(user);
      this.googleAnalyticsService.set_user(user.id);
      return user;
    }
  }

  login(email: string, password: string, email_token = ''): Observable<User>  {
    const body = { email, password, email_token };
    return this.http.post<any>(this.login_url, body)
      .pipe(map(userDict => {
          return this.loadUser(userDict);
      }));
  }

  refresh(): Observable<User> {
    // For a refresh, we'll hold to the existing token, and try to make the request.
    return this.http.get<any>(this.refresh_url)
      .pipe(map(userDict => {
        userDict.token = this.token;
        return this.loadUser(userDict);
      }),
      );
  }

  resetPassword(newPassword: string, email_token: string): Observable<any>  {
    const reset = { password: newPassword, email_token: email_token };
    return this.http.post<any>(this.reset_pass_url, reset)
      .pipe(map(userDict => {
          return this.loadUser(userDict);
      }));
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem(AuthenticationService.LOCAL_TOKEN_KEY);
    this.currentUserSubject.next(null);
    this.googleAnalyticsService.set_user(null);
  }


}
