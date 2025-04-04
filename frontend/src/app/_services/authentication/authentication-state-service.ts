import {Injectable, signal, WritableSignal} from '@angular/core';
import {User} from '@models/user';

/**
 * Authentication Service
 *
 * Separates user login state from actual authentication logic (see AuthenticationService) to avoid
 * circular dependency errors in the HTTP interceptors.
 */
@Injectable({providedIn: 'root'})
export class AuthenticationStateService {
  public static LOCAL_TOKEN_KEY = 'star_token';
  public currentUser: WritableSignal<User | undefined> = signal(undefined);

  constructor() {}

  get authToken(): string {
    return localStorage.getItem(AuthenticationStateService.LOCAL_TOKEN_KEY);
  }

  set authToken(token: string) {
    localStorage.setItem(AuthenticationStateService.LOCAL_TOKEN_KEY, token);
  }

  /** Adds user token to local storage to log user in. */
  setUser(user: User): void {
    this.authToken = user.token;
    this.currentUser.set(user);
  }

  /** Removes user from local storage to log user out. */
  removeUser() {
    localStorage.removeItem(AuthenticationStateService.LOCAL_TOKEN_KEY);
    this.currentUser.set(undefined);
  }
}
