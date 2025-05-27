import {inject, Injectable, signal, WritableSignal} from '@angular/core';
import {User} from '@app/shared/models/user';
import {StorageService} from '@app/shared/services/storage/storage.service';

/**
 * Authentication Service
 *
 * Separates user login state from actual authentication logic (see AuthenticationService) to avoid
 * circular dependency errors in the HTTP interceptors.
 */
@Injectable({providedIn: 'root'})
export class AuthenticationStateService {
  public static LOCAL_TOKEN_KEY = 'star_token';
  public static LOCAL_TOKEN_URL_KEY = 'token_url';
  public currentUser: WritableSignal<User | undefined> = signal(undefined);
  public storageService = inject(StorageService);

  constructor() {}

  get authToken(): string {
    return this.storageService.get(AuthenticationStateService.LOCAL_TOKEN_KEY);
  }

  set authToken(token: string) {
    this.storageService.set(AuthenticationStateService.LOCAL_TOKEN_KEY, token);
  }

  /** Adds user token to local storage to log user in. */
  setUser(user: User): void {
    this.authToken = user.token;
    this.currentUser.set(user);
  }

  /** Removes user from local storage to log user out. */
  removeUser() {
    this.storageService.remove(AuthenticationStateService.LOCAL_TOKEN_KEY);
    this.currentUser.set(undefined);
  }
}
