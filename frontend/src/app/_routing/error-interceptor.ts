import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {Router} from '@angular/router';


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  isSession = new RegExp('.*/api/session');


  constructor(private router: Router) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError(err => {
      // Redirect user to logged out page if they are making a
      // request and get a 401. But don't do it for session calls
      // which are trying to refresh user accounts - as is the case
      // when they first return after being logged out for a while.
      if (err.status === 401 && !this.isSession.test(request.url)) {
        console.log('Unauthorized Access!!!', request);
        // auto logout if 401 response returned from api
        this.router.navigate(['timedout']);
      }

      const error = err.error.message || err.statusText;
      return throwError(error);
    }));
  }
}
