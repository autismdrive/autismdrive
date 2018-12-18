import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { Study } from './study';
import { Resource } from './resource';
import { Training } from './training';
import { User } from './user';

@Injectable()
export class ApiService {

  apiRoot = environment.api;

  // REST endpoints
  endpoints = {
    studyList: '/api/study',
    study: '/api/study/<id>',
    resourceList: '/api/resource',
    resource: '/api/resource/<id>',
    trainingList: '/api/training',
    training: '/api/training/<id>',
    login_password: '/api/login_password',
    forgot_password: '/api/forgot_password',
    reset_password: '/api/reset_password',
    session: '/api/session',
    userList: '/api/user',
  };

  private hasSession: boolean;
  private sessionSubject = new BehaviorSubject<User>(null);

  constructor(private httpClient: HttpClient) {
  }


  /** getSession */
  public getSession(): Observable<User> {
    if (!this.hasSession && localStorage.getItem('token')) {
      this._fetchSession();
    }
    return this.sessionSubject.asObservable();
  }

  /** _fetchSession */
  public _fetchSession(): void {
    this.httpClient.get<User>(this.apiRoot + this.endpoints.session).subscribe(user => {
      this.hasSession = true;
      this.sessionSubject.next(user);
    }, (error) => {
      localStorage.removeItem('token');
      this.hasSession = false;
      this.sessionSubject.error(error);
    });
  }

  /** openSession */
  openSession(token: string): Observable<User> {
    localStorage.setItem('token', token);
    return this.getSession();
  }

  /** closeSession */
  closeSession(): Observable<User> {
    this.httpClient.delete<User>(this.apiRoot + this.endpoints.session).subscribe(x => {
      localStorage.removeItem('token');
      sessionStorage.clear();
      this.hasSession = false;
      this.sessionSubject.next(null);
    }, (error) => {
      localStorage.removeItem('token');
      sessionStorage.clear();
      this.hasSession = false;
      this.sessionSubject.error(error);
    });
    return this.sessionSubject.asObservable();
  }

  /** loginUser - allow users to log into the system with a user name and password.
   * email_token is not required, only send this if user is logging in for the first time
   * after an email verification link. */
  login(email: string, password: string, email_token = ''): Observable<any> {
    const options = { email: email, password: password, email_token: email_token };
    return this.httpClient.post(this.apiRoot + this.endpoints.login_password, options)
      .pipe(catchError(this.handleError));
  }

  /** resetPassword
   * Reset password */
  resetPassword(newPassword: string, email_token: string): Observable<string> {
    const reset = { password: newPassword, email_token: email_token };
    return this.httpClient.post<string>(this.apiRoot + this.endpoints.reset_password, reset)
      .pipe(catchError(this.handleError));
  }

  /** sendResetPasswordEmail
   * Reset password */
  sendResetPasswordEmail(email: String): Observable<any> {
    const email_data = { email: email };
    return this.httpClient.post<any>(this.apiRoot + this.endpoints.forgot_password, email_data)
      .pipe(catchError(this.handleError));
  }

  // Add Study
  addStudy(study: Study): Observable<Study> {
    console.log('adding a study:', study);
    return this.httpClient.post<Study>(this.apiRoot + this.endpoints.studyList, study)
      .pipe(catchError(this.handleError));
  }

  // Update Study
  updateStudy(study: Study): Observable<Study> {
    console.log('updating a study:', study);
    return this.httpClient.put<Study>(`${this.apiRoot + this.endpoints.study}/${study.id}`, study)
      .pipe(catchError(this.handleError));
  }

  // Delete Study
  deleteStudy(study: Study): Observable<Study> {
    console.log('deleting a study:', study);
    return this.httpClient.delete<Study>(`${this.apiRoot + this.endpoints.study}/${study.id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Study
  getStudy(id: number): Observable<Study> {
    console.log('getting Study number ', id);
    return this.httpClient.get<Study>(`${this.apiRoot + this.endpoints.study}/${id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Studies
  getStudies(): Observable<Study[]> {
    console.log('getting a list of Studies');
    return this.httpClient.get<Study[]>(this.apiRoot + this.endpoints.studyList)
      .pipe(catchError(this.handleError));
  }

  // Add Resource
  addResource(resource: Resource): Observable<Resource> {
    console.log('adding a resource:', resource);
    return this.httpClient.post<Resource>(this.apiRoot + this.endpoints.resourceList, resource)
      .pipe(catchError(this.handleError));
  }

  // Update resource
  updateResource(resource: Resource): Observable<Resource> {
    console.log('updating a resource:', resource);
    return this.httpClient.put<Resource>(`${this.apiRoot + this.endpoints.resource}/${resource.id}`, resource)
      .pipe(catchError(this.handleError));
  }

  // Delete Resource
  deleteResource(resource: Resource): Observable<Resource> {
    console.log('deleting a resource:', resource);
    return this.httpClient.delete<Resource>(`${this.apiRoot + this.endpoints.resource}/${resource.id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Resource
  getResource(id: number): Observable<Resource> {
    console.log('getting resource number ', id);
    return this.httpClient.get<Resource>(`${this.apiRoot + this.endpoints.resource}/${id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Resources
  getResources(): Observable<Resource[]> {
    console.log('getting a list of resources');
    return this.httpClient.get<Resource[]>(this.apiRoot + this.endpoints.resourceList)
      .pipe(catchError(this.handleError));
  }

  // Add Training
  addTraining(training: Training): Observable<Training> {
    console.log('adding a training:', training);
    return this.httpClient.post<Training>(this.apiRoot + this.endpoints.trainingList, training)
      .pipe(catchError(this.handleError));
  }

  // Update Training
  updateTraining(training: Training): Observable<Training> {
    console.log('updating a training:', training);
    return this.httpClient.put<Training>(`${this.apiRoot + this.endpoints.training}/${training.id}`, training)
      .pipe(catchError(this.handleError));
  }

  // Delete Training
  deleteTraining(training: Training): Observable<Training> {
    console.log('deleting a training:', training);
    return this.httpClient.delete<Training>(`${this.apiRoot + this.endpoints.training}/${training.id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Training
  getTraining(id: number): Observable<Training> {
    console.log('getting training number ', id);
    return this.httpClient.get<Training>(`${this.apiRoot + this.endpoints.training}/${id}`)
      .pipe(catchError(this.handleError));
  }

  // Get Trainings
  getTrainings(): Observable<Training[]> {
    console.log('getting a list of trainings');
    return this.httpClient.get<Training[]>(this.apiRoot + this.endpoints.trainingList)
      .pipe(catchError(this.handleError));
  }

  // addUser
  addUser(user: User): Observable<User> {
    return this.httpClient.post<User>(this.apiRoot + this.endpoints.userList, user)
      .pipe(catchError(this.handleError));
  }


  private handleError(error: HttpErrorResponse) {
    let message = 'Something bad happened; please try again later.';
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned a status code ${error.status}, ` +
        `Code was: ${JSON.stringify(error.error.code)}, ` +
        `Message was: ${JSON.stringify(error.error.message)}`);
      message = error.error.message;
    }
    // return an observable with a user-facing error message
    // FIXME: Log all error messages to Google Analytics
    return throwError(message);
  }
}
