import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from '../../_models/user';
import { environment } from '../../../environments/environment';
import { GoogleAnalyticsService } from '../../google-analytics.service';



@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  public static LOCAL_TOKEN_KEY = 'star_token';
  private currentUserSubject: Subject<User>;
  public currentUser: Observable<User>;

  login_url = `${environment.api}/api/login_password`;
  reset_pass_url = `${environment.api}/api/reset_password`;
  refresh_url = `${environment.api}/api/session`;


  constructor(private http: HttpClient, private googleAnalyticsService: GoogleAnalyticsService) {
    const token = localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY);
    this.currentUserSubject = new BehaviorSubject<User>(null);
    this.currentUser = this.currentUserSubject.asObservable();
    if (token) {
      console.log('A token is set.  Grabbing the user.');
      this._refresh().subscribe();  // Make sure the api still considers the in-memory user as valid.
    } else {
      console.log('No Token.  Current user is null.');
      this.currentUserSubject.next(null);
    }
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

  login(email: string, password: string, email_token = ''): Observable<User>  {
    const body = { email, password, email_token };
    return this.http.post<any>(this.login_url, body)
      .pipe(map(userDict => {
          return this.loadUser(userDict);
      }));
  }

  private _refresh(): Observable<User> {
    // For a refresh, we'll hold to the existing token, and try to make the request.
    return this.http.get<any>(this.refresh_url)
      .pipe(map(userDict => {
        return this.loadUser(userDict);
      }, error => {
        this.currentUserSubject.next(null);
        }),
      );
  }

  refresh() {
    this._refresh().subscribe();
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
