import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import {AuthenticationService} from '../_services/api/authentication-service';


@Injectable()
export class JwtInterceptor implements HttpInterceptor {

  isS3 = new RegExp('^https?:\/\/s3.amazonaws.com.*');

  constructor(private authenticationService: AuthenticationService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with jwt token if available
    const currentUser = this.authenticationService.currentUserValue;

    if (this.isS3.test(request.url)) {
      // NOOP - don't add authorization headers when making s3 requests, it confuses AWS.
    } else if (currentUser && currentUser.token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${currentUser.token}`
        }
      });
    }

    return next.handle(request);
  }
}
