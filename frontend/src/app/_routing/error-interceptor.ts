import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Router} from '@angular/router';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {StarError} from '../star-error';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  isSession = new RegExp('.*/api/session|.*/logout|.*/timedout');

  constructor(
    private router: Router,
    private googleAnalyticsService: GoogleAnalyticsService,
    private authenticationService: AuthenticationService,
  ) {}

  private logError(error: StarError) {
    console.error(error);
    this.googleAnalyticsService.errorEvent(error);
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError(err => {
        // Redirect user to logged out page if they are making a
        // request and get a 401. But don't do it for session calls
        // which are trying to refresh user accounts - as is the case
        // when they first return after being logged out for a while.
        if (err.status === 401 && !this.isSession.test(request.url)) {
          // Skip if they already know they're logged out.
          if (this.authenticationService.currentUser && localStorage.getItem(AuthenticationService.LOCAL_TOKEN_KEY)) {
            console.error('Unauthorized Access', request);
            this.router.navigate(['timedout']);
          }
        }

        // Log error to google if possible
        if (err.error) {
          this.logError(err.error);
        }

        // You can put anything in an Error.  In this case we are putting an error
        // object with a code and a message.
        const error = err.error || err.statusText;
        return throwError(error);
      }),
    );
  }
}
