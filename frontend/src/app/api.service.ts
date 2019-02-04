import {
  HttpClient,
  HttpErrorResponse,
  HttpEvent,
  HttpEventType,
  HttpHeaders,
  HttpParams
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError, of as observableOf } from 'rxjs';
import { catchError, last, map } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { Resource } from './resource';
import { Study } from './study';
import { Training } from './training';
import { User } from './user';
import { Participant } from './participant';

@Injectable()
export class ApiService {

  apiRoot = environment.api;

  // REST endpoints
  endpoints = {
    categorybyresource: '/api/resource/<resource_id>/category',
    categorybystudy: '/api/study/<study_id>/category',
    categorybytraining: '/api/training/<training_id>/category',
    category: '/api/category/<id>',
    categorylist: '/api/category',
    flow: '/api/flow/<name>/<participant_id>',
    flowlist: '/api/flow',
    flowquestionnaire: '/api/flow/<flow>/<questionnaire_name>',
    organization: '/api/organization/<id>',
    organizationlist: '/api/organization',
    participantbysession: '/api/session/participant/<relationship>',
    participant: '/api/participant/<id>',
    questionnaire: '/api/q/<name>/<id>',
    questionnairemeta: '/api/q/<name>/meta',
    resourcebycategory: '/api/category/<category_id>/resource',
    resourcecategory: '/api/resource_category/<id>',
    resourcecategorylist: '/api/resource_category',
    resource: '/api/resource/<id>',
    resourcelist: '/api/resource',
    rootcategorylist: '/api/category/root',
    session: '/api/session',
    studybycategory: '/api/category/<category_id>/study',
    studycategory: '/api/study_category/<id>',
    studycategorylist: '/api/study_category',
    study: '/api/study/<id>',
    studylist: '/api/study',
    trainingbycategory: '/api/category/<category_id>/training',
    trainingcategory: '/api/training_category/<id>',
    trainingcategorylist: '/api/training_category',
    training: '/api/training/<id>',
    traininglist: '/api/training',
    user: '/api/user/<id>',
    userlist: '/api/user',
    userparticipant: '/api/user_participant/<id>',
    forgot_password: '/api/forgot_password',
    login_password: '/api/login_password',
    reset_password: '/api/reset_password',
  };

  constructor(private httpClient: HttpClient) {
  }

  /** getSession */
  public getSession(): Observable<User> {
    if (localStorage.getItem('token')) {
      return this.httpClient.get<User>(this._endpointUrl('session'))
        .pipe(catchError(this.handleError));
    } else {
      return observableOf(null);
    }
  }

  /** openSession */
  openSession(token: string): Observable<User> {
    localStorage.setItem('token', token);
    return this.getSession();
  }

  /** closeSession */
  closeSession(): Observable<User> {
    if (localStorage.getItem('token')) {
      localStorage.clear();
      sessionStorage.clear();
      return this.httpClient.delete<User>(this._endpointUrl('session'));
    } else {
      localStorage.clear();
      sessionStorage.clear();
      return observableOf(null);
    }
  }

  /** loginUser - allow users to log into the system with a user name and password.
   * email_token is not required, only send this if user is logging in for the first time
   * after an email verification link. */
  login(email: string, password: string, email_token = ''): Observable<any> {
    const options = { email: email, password: password, email_token: email_token };
    return this.httpClient.post(this._endpointUrl('login_password'), options)
      .pipe(catchError(this.handleError));
  }

  /** resetPassword
   * Reset password */
  resetPassword(newPassword: string, email_token: string): Observable<string> {
    const reset = { password: newPassword, email_token: email_token };
    return this.httpClient.post<string>(this._endpointUrl('reset_password'), reset)
      .pipe(catchError(this.handleError));
  }

  /** sendResetPasswordEmail
   * Reset password */
  sendResetPasswordEmail(email: string): Observable<any> {
    const email_data = { email: email };
    return this.httpClient.post<any>(this._endpointUrl('forgot_password'), email_data)
      .pipe(catchError(this.handleError));
  }

  /** addParticipant */
  addParticipant(relationship: string, participant: Participant): Observable<Participant> {
    const url = this
      ._endpointUrl('participantbysession')
      .replace('<relationship>', relationship);
    return this.httpClient.post<Participant>(url, participant);
  }

  // Add Study
  addStudy(study: Study): Observable<Study> {
    return this.httpClient.post<Study>(this._endpointUrl('studylist'), study)
      .pipe(catchError(this.handleError));
  }

  /** Update Study */
  updateStudy(study: Study): Observable<Study> {
    return this.httpClient.put<Study>(`${this._endpointUrl('study')}/${study.id}`, study)
      .pipe(catchError(this.handleError));
  }

  /** Delete Study */
  deleteStudy(study: Study): Observable<Study> {
    return this.httpClient.delete<Study>(`${this._endpointUrl('study')}/${study.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Study */
  getStudy(id: number): Observable<Study> {
    return this.httpClient.get<Study>(this._endpointUrl('study').replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Studies */
  getStudies(): Observable<Study[]> {
    return this.httpClient.get<Study[]>(this._endpointUrl('studylist'))
      .pipe(catchError(this.handleError));
  }

  /** Add Resource */
  addResource(resource: Resource): Observable<Resource> {
    return this.httpClient.post<Resource>(this._endpointUrl('resourcelist'), resource)
      .pipe(catchError(this.handleError));
  }

  /** Update resource */
  updateResource(resource: Resource): Observable<Resource> {
    return this.httpClient.put<Resource>(`${this._endpointUrl('resource')}/${resource.id}`, resource)
      .pipe(catchError(this.handleError));
  }

  /** Delete Resource */
  deleteResource(resource: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(`${this._endpointUrl('resource')}/${resource.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Resource */
  getResource(id: number): Observable<Resource> {
    return this.httpClient.get<Resource>(this._endpointUrl('resource').replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Resources */
  getResources(): Observable<Resource[]> {
    return this.httpClient.get<Resource[]>(this._endpointUrl('resourcelist'))
      .pipe(catchError(this.handleError));
  }

  /** Add Training */
  addTraining(training: Training): Observable<Training> {
    return this.httpClient.post<Training>(this._endpointUrl('traininglist'), training)
      .pipe(catchError(this.handleError));
  }

  /** Update Training */
  updateTraining(training: Training): Observable<Training> {
    return this.httpClient.put<Training>(`${this._endpointUrl('training')}/${training.id}`, training)
      .pipe(catchError(this.handleError));
  }

  /** Delete Training */
  deleteTraining(training: Training): Observable<Training> {
    return this.httpClient.delete<Training>(`${this._endpointUrl('training')}/${training.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Training */
  getTraining(id: number): Observable<Training> {
    return this.httpClient.get<Training>(this._endpointUrl('training').replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Trainings */
  getTrainings(): Observable<Training[]> {
    return this.httpClient.get<Training[]>(this._endpointUrl('traininglist'))
      .pipe(catchError(this.handleError));
  }

  // addUser
  addUser(user: User): Observable<User> {
    return this.httpClient.post<User>(this._endpointUrl('userlist'), user)
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

  /** getQuestionnaire */
  getQuestionnaire(key: string, id: number) {
    return this.httpClient.get<object>(this._qEndpoint('', key, id))
      .pipe(catchError(this.handleError));
  }

  /** updateQuestionnaire */
  updateQuestionnaire(key: string, id: number, options: object) {
    return this.httpClient.put<object>(this._qEndpoint('', key, id), options)
      .pipe(catchError(this.handleError));
  }

  /** getQuestionnaireMeta */
  getQuestionnaireMeta(key: string) {
    return this.httpClient.get<any>(this._qEndpoint('meta', key))
      .pipe(catchError(this.handleError));
  }

  /** getQuestionnaireList */
  getQuestionnaireList(key: string) {
    return this.httpClient.get<object>(this._qEndpoint('list', key))
      .pipe(catchError(this.handleError));
  }

  /** submitQuestionnaire */
  submitQuestionnaire(key: string, options: object) {
    return this.httpClient.post<object>(this._qEndpoint('list', key), options)
      .pipe(catchError(this.handleError));
  }

  private _endpointUrl(endpointName: string): string {
    const path = this.endpoints[endpointName];

    if (path) {
      return this.apiRoot + path;
    } else {
      console.log(`endpoint '${endpointName}' does not exist`);
    }
  }

  private _qEndpoint(eType = '', qName: string, qId?: number) {
    // Capitalize first letter of endpoint
    if (eType !== '') {
      eType = eType.charAt(0).toUpperCase() + eType.slice(1);
    }

    const path = this
      .endpoints['questionnaire' + eType]
      .replace('<name>', qName + '_questionnaire')
      .replace('<id>', isFinite(qId) ? qId.toString() : '');

    return this.apiRoot + path;
  }

}
