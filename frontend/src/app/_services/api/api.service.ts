import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of as observableOf, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { EmailLog } from '../../_models/email_log'
import { Flow } from '../../_models/flow';
import { Participant } from '../../_models/participant';
import { Query } from '../../_models/query';
import { Resource } from '../../_models/resource';
import { Study } from '../../_models/study';
import { StepLog } from '../../_models/step_log'
import { User } from '../../_models/user';
import { UserSearchResults } from '../../_models/user_search_results';
import { environment } from '../../../environments/environment';

@Injectable()
export class ApiService {

  apiRoot = environment.api;

  // REST endpoints
  endpoints = {
    categorybyresource: '/api/resource/<resource_id>/category',
    categorybystudy: '/api/study/<study_id>/category',
    category: '/api/category/<id>',
    categorylist: '/api/category',
    flow: '/api/flow/<name>/<participant_id>',
    flowAnonymous: '/api/flow/<name>',
    flowlist: '/api/flow',
    flowquestionnaire: '/api/flow/<flow>/<questionnaire_name>',
    flowquestionnairemeta: '/api/flow/<flow>/<questionnaire_name>/meta',
    organization: '/api/organization/<id>',
    organizationlist: '/api/organization',
    participantbysession: '/api/session/participant',
    participant: '/api/participant/<id>',
    participantStepLog: '/api/participant/step_log/<id>',
    questionnaire: '/api/q/<name>/<id>',
    questionnaireList: '/api/q/<name>',
    questionnaireListMeta: '/api/q/<name>/meta',
    questionnaireNames: '/api/q',
    questionnaireExport: '/api/q/<name>/export',
    questionnairemeta: '/api/flow/<flow>/<questionnaire_name>/meta',
    eventbycategory: '/api/category/<category_id>/event',
    eventcategory: '/api/event_category/<id>',
    eventcategorylist: '/api/event_category',
    event: '/api/event/<id>',
    eventlist: '/api/event',
    locationbycategory: '/api/category/<category_id>/location',
    locationcategory: '/api/location_category/<id>',
    locationcategorylist: '/api/location_category',
    location: '/api/location/<id>',
    locationlist: '/api/location',
    resourcebycategory: '/api/category/<category_id>/resource',
    resourcecategory: '/api/resource_category/<id>',
    resourcecategorylist: '/api/resource_category',
    resource: '/api/resource/<id>',
    resourcelist: '/api/resource',
    rootcategorylist: '/api/category/root',
    search: '/api/search',
    session: '/api/session',
    sessionstatus: '/api/session/status',
    sessionparticipants: '/api/session/participant',
    studybycategory: '/api/category/<category_id>/study',
    studycategory: '/api/study_category/<id>',
    studycategorylist: '/api/study_category',
    study: '/api/study/<id>',
    studylist: '/api/study',
    user: '/api/user/<id>',
    userEmailLog: '/api/user/email_log/<id>',
    userlist: '/api/user',
    userparticipant: '/api/user_participant/<id>',
    forgot_password: '/api/forgot_password',
  };

  constructor(private httpClient: HttpClient) {
  }

  private _handleError(error: HttpErrorResponse) {
    const message = 'Something bad happened; please try again later.';

    console.error(error);

    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      let errorMessage = `Backend returned a status code ${error.status}, `;
      if (error.error) {
        errorMessage +=
          `Code was: ${JSON.stringify(error.error.code)}, ` +
          `Message was: ${JSON.stringify(error.error.message)}`;
      }
      console.error(errorMessage);
    }
    // return an observable with a user-facing error message
    // FIXME: Log all error messages to Google Analytics
    return throwError(message);
  }

  /** sendResetPasswordEmail
   * Reset password */
  sendResetPasswordEmail(email: string): Observable<any> {
    const email_data = { email: email };
    return this.httpClient.post<any>(this._endpointUrl('forgot_password'), email_data)
      .pipe(catchError(this._handleError));
  }

  /** addParticipant */
  addParticipant(participant: Participant): Observable<Participant> {
    const url = this
      ._endpointUrl('participantbysession');
    return this.httpClient.post<Participant>(url, participant)
      .pipe(
        map(participantJson => new Participant(participantJson)),
        catchError(this._handleError));
  }

  /** updateParticipant */
  updateParticipant(participant: Participant): Observable<Participant> {
    return this.httpClient.put<Participant>(this._endpointUrl('participant').replace('<id>', participant.id.toString()), participant)
      .pipe(catchError(this._handleError));
  }

  /** Get Participant */
  getParticipant(id: number): Observable<Participant> {
    return this.httpClient.get<Participant>(this._endpointUrl('participant').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** getFlow */
  getFlow(flow: string, participantId?: number): Observable<Flow> {
    let url = '';
    if (participantId) {
      url = this
        ._endpointUrl('flow')
        .replace('<name>', flow)
        .replace('<participant_id>', participantId.toString());
    } else {
      url = this
        ._endpointUrl('flowAnonymous')
        .replace('<name>', flow);
    }
    return this.httpClient.get<Flow>(url)
      .pipe(
        map(json => new Flow(json)),
        catchError(this._handleError));
  }

  // Add Study
  addStudy(study: Study): Observable<Study> {
    return this.httpClient.post<Study>(this._endpointUrl('studylist'), study)
      .pipe(catchError(this._handleError));
  }

  /** Update Study */
  updateStudy(study: Study): Observable<Study> {
    return this.httpClient.put<Study>(`${this._endpointUrl('study')}/${study.id}`, study)
      .pipe(catchError(this._handleError));
  }

  /** Delete Study */
  deleteStudy(study: Study): Observable<Study> {
    return this.httpClient.delete<Study>(`${this._endpointUrl('study')}/${study.id}`)
      .pipe(catchError(this._handleError));
  }

  /** Get Study */
  getStudy(id: number): Observable<Study> {
    return this.httpClient.get<Study>(this._endpointUrl('study').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get Studies */
  getStudies(): Observable<Study[]> {
    return this.httpClient.get<Study[]>(this._endpointUrl('studylist'))
      .pipe(catchError(this._handleError));
  }

  /** Add Event */
  addEvent(event: Resource): Observable<Resource> {
    return this.httpClient.post<Resource>(this._endpointUrl('eventlist'), event)
      .pipe(catchError(this._handleError));
  }

  /** Update Event */
  updateEvent(event: Resource): Observable<Resource> {
    return this.httpClient.put<Resource>(`${this._endpointUrl('event')}/${event.id}`, event)
      .pipe(catchError(this._handleError));
  }

  /** Delete Event */
  deleteEvent(event: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(`${this._endpointUrl('event')}/${event.id}`)
      .pipe(catchError(this._handleError));
  }

  /** Get Event */
  getEvent(id: number): Observable<Resource> {
    return this.httpClient.get<Resource>(this._endpointUrl('event').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get Events */
  getEvents(): Observable<Resource[]> {
    return this.httpClient.get<Resource[]>(this._endpointUrl('eventlist'))
      .pipe(catchError(this._handleError));
  }

  /** Add Location */
  addLocation(location: Resource): Observable<Resource> {
    return this.httpClient.post<Resource>(this._endpointUrl('locationlist'), location)
      .pipe(catchError(this._handleError));
  }

  /** Update Location */
  updateLocation(location: Resource): Observable<Resource> {
    return this.httpClient.put<Resource>(`${this._endpointUrl('location')}/${location.id}`, location)
      .pipe(catchError(this._handleError));
  }

  /** Delete Location */
  deleteLocation(location: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(`${this._endpointUrl('location')}/${location.id}`)
      .pipe(catchError(this._handleError));
  }

  /** Get Location */
  getLocation(id: number): Observable<Resource> {
    return this.httpClient.get<Resource>(this._endpointUrl('location').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get Locations */
  getLocations(): Observable<Resource[]> {
    return this.httpClient.get<Resource[]>(this._endpointUrl('locationlist'))
      .pipe(catchError(this._handleError));
  }

  /** Add Resource */
  addResource(resource: Resource): Observable<Resource> {
    return this.httpClient.post<Resource>(this._endpointUrl('resourcelist'), resource)
      .pipe(catchError(this._handleError));
  }

  /** Update resource */
  updateResource(resource: Resource): Observable<Resource> {
    return this.httpClient.put<Resource>(`${this._endpointUrl('resource')}/${resource.id}`, resource)
      .pipe(catchError(this._handleError));
  }

  /** Delete Resource */
  deleteResource(resource: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(`${this._endpointUrl('resource')}/${resource.id}`)
      .pipe(catchError(this._handleError));
  }

  /** Get Resource */
  getResource(id: number): Observable<Resource> {
    return this.httpClient.get<Resource>(this._endpointUrl('resource').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get Resources */
  getResources(): Observable<Resource[]> {
    return this.httpClient.get<Resource[]>(this._endpointUrl('resourcelist'))
      .pipe(catchError(this._handleError));
  }

  /** Get User */
  getUser(id: number): Observable<User> {
    return this.httpClient.get<User>(this._endpointUrl('user').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** addUser */
  addUser(user: User): Observable<User> {
    return this.httpClient.post<User>(this._endpointUrl('userlist'), user)
      .pipe(
        map(json => new User(json)),
        catchError(this._handleError));
  }

  /** findUsers */
  findUsers(filter = '', sort = 'email', sortOrder = 'asc', pageNumber = 0, pageSize = 3): Observable<UserSearchResults> {
    const search_data = { filter: filter, sort: sort, sortOrder: sortOrder, pageNumber: String(pageNumber), pageSize: String(pageSize) };
    return this.httpClient.get<UserSearchResults>(this._endpointUrl('userlist'), { params: search_data })
      .pipe(catchError(this._handleError));
  }

  /** Get User Email Log */
  getUserEmailLog(user: User): Observable<EmailLog[]> {
    return this.httpClient.get<EmailLog[]>(this._endpointUrl('userEmailLog').replace('<id>', user.id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get Participant Step Log */
  getParticipantStepLog(participant: Participant): Observable<StepLog[]> {
    return this.httpClient.get<StepLog[]>(this._endpointUrl('participantStepLog').replace('<id>', participant.id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** getQuestionnaireNames */
  getQuestionnaireNames() {
    const url = this
      ._endpointUrl('questionnaireNames');
    return this.httpClient.get<any>(url)
      .pipe(catchError(this._handleError));
  }

  /** getQuestionnaireList */
  getQuestionnaireList(name: string) {
    const url = this
      ._endpointUrl('questionnaireList')
      .replace('<name>', name);
    return this.httpClient.get<object>(url)
      .pipe(catchError(this._handleError));
  }

  /** getQuestionnaireListMeta */
  getQuestionnaireListMeta(name: string) {
    const url = this
      ._endpointUrl('questionnaireListMeta')
      .replace('<name>', name);
    return this.httpClient.get<object>(url)
      .pipe(catchError(this._handleError));
  }

  /** exportQuestionnaire */
  exportQuestionnaire(name: string): Observable<any> {
    const url = this
      ._endpointUrl('questionnaireExport')
      .replace('<name>', name);
    return this.httpClient.get(url, { observe: 'response', responseType: 'blob' as 'json' });
    // .pipe(catchError(this._handleError));
  }

  /** getQuestionnaire */
  getQuestionnaire(name: string, id: number) {
    const url = this
      ._endpointUrl('questionnaire')
      .replace('<name>', name)
      .replace('<id>', id.toString());
    return this.httpClient.get<object>(url)
      .pipe(catchError(this._handleError));
  }

  /** updateQuestionnaire */
  updateQuestionnaire(name: string, id: number, options: object) {
    const url = this._endpointUrl('questionnaire')
      .replace('<name>', name)
      .replace('<id>', id.toString());
    return this.httpClient.put<object>(url, options)
      .pipe(catchError(this._handleError));
  }

  /** getQuestionnaireMeta */
  getQuestionnaireMeta(flow: string, questionnaire_name: string) {
    const url = this._endpointUrl('questionnairemeta')
      .replace('<flow>', flow)
      .replace('<questionnaire_name>', questionnaire_name);
    return this.httpClient.get<any>(url)
      .pipe(catchError(this._handleError));
  }

  /** submitQuestionnaire */
  submitQuestionnaire(flow: string, questionnaire_name: string, options: object) {
    const url = this
      ._endpointUrl('flowquestionnaire')
      .replace('<flow>', flow)
      .replace('<questionnaire_name>', questionnaire_name);
    return this.httpClient.post<object>(url, options)
      .pipe(catchError(this._handleError));
  }

  search(query: Query): Observable<Query> {
    const url = this._endpointUrl('search');
    return this.httpClient.post<Query>(url, query)
      .pipe(catchError(this._handleError));
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
