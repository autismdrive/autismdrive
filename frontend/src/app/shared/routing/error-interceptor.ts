import {HttpEvent, HttpHandlerFn, HttpRequest} from '@angular/common/http';
import {forwardRef, inject} from '@angular/core';
import {Router} from '@angular/router';
import {AuthenticationStateService} from '@app/shared/services/authentication/authentication-state-service';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {ApiError} from '../../api-error';

export function errorInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const router = inject(forwardRef(() => Router));
  const authenticationStateService = inject(forwardRef(() => AuthenticationStateService));
  const isSession = new RegExp('.*/api/session|.*/logout|.*/timedout');

  return next(req).pipe(
    catchError(err => {
      // Redirect user to logged out page if they are making a
      // request and get a 401. But don't do it for session calls
      // which are trying to refresh user accounts - as is the case
      // when they first return after being logged out for a while.
      if (err.status === 401 && !isSession.test(req.url)) {
        // Skip if they already know they're logged out.
        if (authenticationStateService.currentUser() && authenticationStateService.authToken) {
          console.error('Unauthorized Access', req);
          router.navigate(['timedout']);
        }
      }

      const apiError: ApiError = err?.error || {code: err.status, message: err.statusText};

      // Ignore config.json errors
      if (req.url !== './config.json') {
        console.error({err});
        return throwError(() => apiError);
      }
    }),
  );
}
