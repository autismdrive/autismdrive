import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/authentication/authentication-service';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  isS3 = new RegExp('^https?://s3.amazonaws.com.*');
  currentUser: User;

  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with jwt token if available
    const token = localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY);

    if (this.isS3.test(request.url)) {
      // NOOP - don't add authorization headers when making s3 requests, it confuses AWS.
    } else if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
    }

    return next.handle(request);
  }
}
