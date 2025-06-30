import {isPlatformServer} from '@angular/common';
import {inject, Injector, PLATFORM_ID} from '@angular/core';
import {toObservable} from '@angular/core/rxjs-interop';
import {ActivatedRouteSnapshot, CanActivateFn, createUrlTreeFromSnapshot, RouterStateSnapshot} from '@angular/router';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';
import {EMPTY, skipWhile, timeout} from 'rxjs';
import {first, map} from 'rxjs/operators';

export const authGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const authService = inject(AuthenticationService);
  const injector = inject(Injector);
  const platformId = inject(PLATFORM_ID);

  return toObservable(authService.status, {injector}).pipe(
    skipWhile(status => status === 'loading'),
    timeout({
      each: 5000,
      with: () => {
        console.error('Auth guard stuck: status did not change from "loading" after 5 seconds.');
        return EMPTY;
      },
    }),
    map(() => {
      if (isPlatformServer(platformId)) {
        // On the server, we cannot determine if the user is logged in.
        // This is because the server does not have access to the user's localStorage or sessionStorage.
        // https://medium.com/@nijotigajo/handling-local-storage-in-angular-with-server-side-rendering-ssr-eaa6a0f11717
        return false;
      }

      if (!!authService.isLoggedIn()) {
        return true;
      }

      return createUrlTreeFromSnapshot(route, ['/', 'login'], {returnUrl: state.url});
    }),
    first(),
  );
};
