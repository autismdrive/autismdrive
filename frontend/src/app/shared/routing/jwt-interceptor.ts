import {HttpEvent, HttpHandlerFn, HttpRequest} from '@angular/common/http';
import {forwardRef, inject} from '@angular/core';
import {AuthenticationStateService} from '@app/shared/services/authentication/authentication-state-service';
import {Observable} from 'rxjs';

export function jwtInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const authStateService = inject(forwardRef(() => AuthenticationStateService));
  const isS3 = new RegExp('^https?:\/\/s3\.amazonaws\.com\/(.*)');

  // add authorization header with jwt token if available
  const token = authStateService.authToken;

  console.log('jwtInterceptor > token:', token);

  if (isS3.test(req.url)) {
    // NOOP - don't add authorization headers when making s3 reqs, it confuses AWS.
  } else if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  return next(req);
}
