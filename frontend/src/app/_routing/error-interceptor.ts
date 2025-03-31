import {HttpEvent, HttpHandlerFn, HttpRequest} from '@angular/common/http';
import {error} from '@angular/compiler-cli/src/transformers/util';
import {inject} from '@angular/core';
import {Router} from '@angular/router';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {ApiError} from '../api-error';

export function errorInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const router = inject(Router);
  const googleAnalyticsService = inject(GoogleAnalyticsService);
  const authenticationService = inject(AuthenticationService);
  const isSession = new RegExp('.*/api/session|.*/logout|.*/timedout');

  return next(req).pipe(
    catchError(err => {
      // Redirect user to logged out page if they are making a
      // request and get a 401. But don't do it for session calls
      // which are trying to refresh user accounts - as is the case
      // when they first return after being logged out for a while.
      if (err.status === 401 && !isSession.test(req.url)) {
        // Skip if they already know they're logged out.
        if (authenticationService.currentUser && localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY)) {
          console.error('Unauthorized Access', req);
          router.navigate(['timedout']);
        }
      }

      const apiError: ApiError = err?.error || {code: err.status, message: err.statusText};

      // Ignore config.json errors
      if (req.url !== './config.json') {
        console.error(err?.error);
        googleAnalyticsService.errorEvent(err?.error);
        return throwError(() => apiError);
      }
    }),
  );
}
