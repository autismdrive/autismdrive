import {HttpEvent, HttpHandlerFn, HttpRequest, HttpResponse, HttpStatusCode} from '@angular/common/http';
import {forwardRef, inject} from '@angular/core';
import {Router} from '@angular/router';
import {ApiError} from '@app/api-error';
import {AuthenticationStateService} from '@app/shared/services/authentication/authentication-state-service';
import {Observable, of, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';

export function errorInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const router: Router = inject(forwardRef(() => Router));
  const authenticationStateService = inject(forwardRef(() => AuthenticationStateService));

  return next(req).pipe(
    catchError(err => {
      const sessionPattern = new RegExp('.*/api/session|.*/logout|.*/timedout');

      // Redirect user to logged out page if they are making a
      // request and get a 401. But don't do it for session calls
      // which are trying to refresh user accounts - as is the case
      // when they first return after being logged out for a while.

      if (err.status === 401 && !sessionPattern.test(req.url)) {
        // Skip if they already know they're logged out.
        if (authenticationStateService.currentUser() && authenticationStateService.authToken) {
          console.error('Unauthorized Access', req);
          // Redirect to timed out page which explains what happened.
          // Return an HttpUserEvent to stop the original request from continuing.
          router.navigate(['/timedout']);
          return of(
            new HttpResponse<boolean>({
              body: false,
              status: HttpStatusCode.TemporaryRedirect,
              statusText: 'Redirecting to timed out page',
              url: router.serializeUrl(router.createUrlTree(['/timedout'])),
            }),
          );
        }
      }

      // Ignore config.json errors
      if (req.url === './config.json') {
        return of(
          new HttpResponse<boolean>({
            body: false,
            status: HttpStatusCode.Ok,
            statusText: 'config.json error ignored',
            url: router.url,
          }),
        );
      }

      // Log all other errors to the console
      console.error({err});
      const apiError: ApiError = err?.error || {code: err.status, message: err.statusText};
      return throwError(() => apiError);
    }),
  );
}
