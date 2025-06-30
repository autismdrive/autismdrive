import {isPlatformServer} from '@angular/common';
import {inject, Injector, PLATFORM_ID} from '@angular/core';
import {toObservable} from '@angular/core/rxjs-interop';
import {ActivatedRouteSnapshot, CanActivateFn, createUrlTreeFromSnapshot, RouterStateSnapshot} from '@angular/router';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {EMPTY, skipWhile, timeout} from 'rxjs';
import {first, map} from 'rxjs/operators';

export const notMirroredGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  // Checks to see if the server we are connected to is running in a mirroring mode.  If so
  // prevent users from taking actions that might cause data issues later on.
  const appEnvironmentService = inject(AppEnvironmentService);
  const authService = inject(AuthenticationService);
  const injector = inject(Injector);
  const platformId = inject(PLATFORM_ID);

  return toObservable(authService.status, {injector}).pipe(
    skipWhile(status => status === 'loading'),
    timeout({
      each: 5000,
      with: () => {
        console.error('notMirroredGuard stuck: status did not change from "loading" after 5 seconds.');
        return EMPTY;
      },
    }),
    map(() => {
      if (isPlatformServer(platformId)) {
        return false;
      }

      if (appEnvironmentService.props() && !appEnvironmentService.mirroring) {
        return createUrlTreeFromSnapshot(route, ['/', 'mirrored']);
      }

      return true;
    }),
    first(),
  );
};
