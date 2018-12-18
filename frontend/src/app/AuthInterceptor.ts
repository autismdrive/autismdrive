/* Intercepts all calls to the backend and assigns an authorization code so we
*  know who this nice person is.  */

// import { AuthService } from '../auth.service';
import { HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  isS3 = new RegExp('^https?:\/\/s3.amazonaws.com.*');

  //  constructor(private auth: AuthService) {}
  constructor() { }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Get the auth token from the service.
    // const authToken = this.auth.getAuthorizationToken();
    const token = localStorage.getItem('token');

    if (this.isS3.test(req.url)) {
      // NOOP - don't add authorization headers when making s3 requests, it confuses AWS.
    } else if (token) {
      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    // send cloned request with header to the next handler.
    return next.handle(req);
  }
}
