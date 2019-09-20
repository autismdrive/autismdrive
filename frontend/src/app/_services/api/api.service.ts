import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable, throwError} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {AdminNote} from '../../_models/admin_note';
import {Category} from '../../_models/category';
import {EmailLog} from '../../_models/email_log';
import {Flow} from '../../_models/flow';
import {Participant} from '../../_models/participant';
import {Query} from '../../_models/query';
import {Resource} from '../../_models/resource';
import {ResourceCategory} from '../../_models/resource_category';
import {Study} from '../../_models/study';
import {StepLog} from '../../_models/step_log';
import {User} from '../../_models/user';
import {UserSearchResults} from '../../_models/user_search_results';
import {environment} from '../../../environments/environment';
import {StudyUser} from '../../_models/study_user';
import {Status} from '../../_models/status';
import {TableInfo} from '../../_models/table_info';
import {DataTransferPageResults} from '../../_models/data_transfer_log';
import {Organization} from '../../_models/organization';
import {StarError} from '../../star-error';
import {GeoLocation} from '../../_models/geolocation';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  apiRoot = environment.api;
  public serverStatus: Observable<Status>;
  // REST endpoints
  public endpoints = {
    adminNote: '/api/admin_note/<id>',
    adminNoteList: '/api/admin_note',
    category: '/api/category/<id>',
    categorybyresource: '/api/resource/<resource_id>/category',
    categorybystudy: '/api/study/<study_id>/category',
    categorylist: '/api/category',
    data_transfer_log: '/api/data_transfer_log',
    event: '/api/event/<id>',
    eventbycategory: '/api/category/<category_id>/event',
    eventcategory: '/api/event_category/<id>',
    eventcategorylist: '/api/event_category',
    eventlist: '/api/event',
    flow: '/api/flow/<name>/<participant_id>',
    flowAnonymous: '/api/flow/<name>',
    flowlist: '/api/flow',
    flowquestionnaire: '/api/flow/<flow>/<questionnaire_name>',
    flowquestionnairemeta: '/api/flow/<flow>/<questionnaire_name>/meta',
    forgot_password: '/api/forgot_password',
    location: '/api/location/<id>',
    locationbycategory: '/api/category/<category_id>/location',
    locationcategory: '/api/location_category/<id>',
    locationcategorylist: '/api/location_category',
    locationlist: '/api/location',
    organization: '/api/organization/<id>',
    organizationlist: '/api/organization',
    participant: '/api/participant/<id>',
    participantbysession: '/api/session/participant',
    participantStepLog: '/api/participant/step_log/<id>',
    questionnaire: '/api/q/<name>/<id>',
    questionnaireExport: '/api/q/<name>/export',
    questionnaireInfo: '/api/q',
    questionnaireList: '/api/q/<name>',
    questionnaireListMeta: '/api/q/<name>/meta',
    questionnaireUserExport: '/api/q/all/export/user/<user_id>',
    questionnairemeta: '/api/flow/<flow>/<questionnaire_name>/meta',
    resource: '/api/resource/<id>',
    resourcebycategory: '/api/category/<category_id>/resource',
    resourcecategory: '/api/resource_category/<id>',
    relatedresources: '/api/resource/<id>/related',
    resourceAdminNoteList: '/api/resource/<resource_id>/admin_note',
    resourcecategorylist: '/api/resource_category',
    resourcelist: '/api/resource',
    rootcategorylist: '/api/category/root',
    search: '/api/search',
    session: '/api/session',
    sessionparticipants: '/api/session/participant',
    sessionstatus: '/api/session/status',
    status: '/api/status',
    study: '/api/study/<id>',
    studybycategory: '/api/category/<category_id>/study',
    studycategory: '/api/study_category/<id>',
    studycategorylist: '/api/study_category',
    studyinquiry: '/api/study_inquiry',
    studylist: '/api/study',
    user: '/api/user/<id>',
    userEmailLog: '/api/user/email_log/<id>',
    userStudyInquiryList: '/api/user/<id>/inquiry/study',
    userAdminNoteList: '/api/user/<user_id>/admin_note',
    userlist: '/api/user',
    userparticipant: '/api/user_participant/<id>',
    zip_code_coords: '/api/zip_code_coords/<id>',
  };
  private statusSubject: BehaviorSubject<Status>;

  constructor(private httpClient: HttpClient) {
    this.statusSubject = new BehaviorSubject<Status>(null);
    this.serverStatus = this.statusSubject.asObservable();
    this.setServerStatus();
  }

  /** sendResetPasswordEmail
   * Reset password */
  sendResetPasswordEmail(email: string): Observable<any> {
    const email_data = {email: email};
    return this.httpClient.post<any>(this._endpointUrl('forgot_password'), email_data)
      .pipe(catchError(this._handleError));
  }

  /** sendStudyInquiryEmail
   * StudyInquiry */
  sendStudyInquiryEmail(user: User, study: Study): Observable<any> {
    const email_data = {user_id: user.id, study_id: study.id};
    return this.httpClient.post<any>(this._endpointUrl('studyinquiry'), email_data)
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
    return this.httpClient.put<Study>(this._endpointUrl('study').replace('<id>', study.id.toString()), study)
      .pipe(catchError(this._handleError));
  }

  /** Delete Study */
  deleteStudy(study: Study): Observable<Study> {
    return this.httpClient.delete<Study>(this._endpointUrl('study').replace('<id>', study.id.toString()))
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

  // Add AdminNote
  addAdminNote(admin_note: AdminNote): Observable<AdminNote> {
    return this.httpClient.post<AdminNote>(this._endpointUrl('adminNoteList'), admin_note)
      .pipe(catchError(this._handleError));
  }

  /** Update AdminNote */
  updateAdminNote(admin_note: AdminNote): Observable<AdminNote> {
    return this.httpClient.put<AdminNote>(this._endpointUrl('adminNote').replace('<id>', admin_note.id.toString()), admin_note)
      .pipe(catchError(this._handleError));
  }

  /** Delete AdminNote */
  deleteAdminNote(admin_note: AdminNote): Observable<AdminNote> {
    return this.httpClient.delete<AdminNote>(this._endpointUrl('adminNote').replace('<id>', admin_note.id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get AdminNote */
  getAdminNote(id: number): Observable<AdminNote> {
    return this.httpClient.get<AdminNote>(this._endpointUrl('adminNote').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get AdminNotes */
  getAdminNotes(): Observable<AdminNote[]> {
    return this.httpClient.get<AdminNote[]>(this._endpointUrl('adminNoteList'))
      .pipe(catchError(this._handleError));
  }

  /** Get AdminNotes by Resource */
  getResourceAdminNotes(resource_id: number): Observable<AdminNote[]> {
    return this.httpClient.get<AdminNote[]>(this._endpointUrl('resourceAdminNoteList').replace('<resource_id>', resource_id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Get AdminNotes by User */
  getUserAdminNotes(user_id: number): Observable<AdminNote[]> {
    return this.httpClient.get<AdminNote[]>(this._endpointUrl('userAdminNoteList').replace('<user_id>', user_id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** Add Event */
  addEvent(event: Resource): Observable<Resource> {
    return this.httpClient.post<Resource>(this._endpointUrl('eventlist'), event)
      .pipe(catchError(this._handleError));
  }

  /** Update Event */
  updateEvent(event: Resource): Observable<Resource> {
    return this.httpClient.put<Resource>(this._endpointUrl('event').replace('<id>', event.id.toString()), event)
      .pipe(catchError(this._handleError));
  }

  /** Delete Event */
  deleteEvent(event: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(this._endpointUrl('event').replace('<id>', event.id.toString()))
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
    return this.httpClient.put<Resource>(this._endpointUrl('location').replace('<id>', location.id.toString()), location)
      .pipe(catchError(this._handleError));
  }

  /** Delete Location */
  deleteLocation(location: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(this._endpointUrl('location').replace('<id>', location.id.toString()))
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
    return this.httpClient.put<Resource>(this._endpointUrl('resource').replace('<id>', resource.id.toString()), resource)
      .pipe(catchError(this._handleError));
  }

  /** Delete Resource */
  deleteResource(resource: Resource): Observable<Resource> {
    return this.httpClient.delete<Resource>(this._endpointUrl('resource').replace('<id>', resource.id.toString()))
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

  /** Get Resources related to the given resource */
  getRelatedResources(id: number): Observable<Resource[]> {
    return this.httpClient.get<Resource[]>(this._endpointUrl('relatedresources').replace('<id>', id.toString()))
      .pipe(catchError(this._handleError));
  }


  /** getResourceCategories */
  getResourceCategories(resource: Resource): Observable<ResourceCategory[]> {
    const url = this._endpointUrl('categorybyresource').replace('<resource_id>', resource.id.toString());
    return this.httpClient.get<ResourceCategory[]>(url)
      .pipe(catchError(this._handleError));
  }

  /** Add ResourceCategory */
  addResourceCategory(resourceCategory: ResourceCategory): Observable<ResourceCategory> {
    return this.httpClient.post<ResourceCategory>(this._endpointUrl('resourcecategorylist'), resourceCategory)
      .pipe(catchError(this._handleError));
  }

  /** Delete ResourceCategory */
  deleteResourceCategory(resourceCategory: ResourceCategory): Observable<ResourceCategory> {
    return this.httpClient.delete<ResourceCategory>(this._endpointUrl('resourcecategory').replace('<id>', resourceCategory.id.toString()))
      .pipe(catchError(this._handleError));
  }

  /** getCategories */
  getCategories(): Observable<Category[]> {
    return this.httpClient.get<Category[]>(this._endpointUrl('categorylist'))
      .pipe(catchError(this._handleError));
  }

  /** getOrganizations */
  getOrganizations(): Observable<Organization[]> {
    return this.httpClient.get<Organization[]>(this._endpointUrl('organizationlist'))
      .pipe(catchError(this._handleError));
  }

  /** Add Organization */
  addOrganization(organization: Organization): Observable<Organization> {
    return this.httpClient.post<Organization>(this._endpointUrl('organizationlist'), organization)
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
    const search_data = {
      filter: filter,
      sort: sort,
      sortOrder: sortOrder,
      pageNumber: String(pageNumber),
      pageSize: String(pageSize)
    };
    return this.httpClient.get<UserSearchResults>(this._endpointUrl('userlist'), {params: search_data})
      .pipe(catchError(this._handleError));
  }

  /** Get User Study Inquiries */
  getUserStudyInquiries(id: number): Observable<StudyUser[]> {
    return this.httpClient.get<StudyUser[]>(this._endpointUrl('userStudyInquiryList').replace('<id>', id.toString()))
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
  getQuestionnaireInfoList() {
    const url = this
      ._endpointUrl('questionnaireInfo');
    return this.httpClient.get<TableInfo[]>(url)
      .pipe(
        map(infoJson => infoJson.map(ij => new TableInfo(ij))),
        catchError(this._handleError));
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
    return this.httpClient.get(url, {observe: 'response', responseType: 'blob' as 'json'});
    // .pipe(catchError(this._handleError));
  }

  /** exportUser Questionnaire */
  exportUserQuestionnaire(user_id:string): Observable<any> {
    const url = this
      ._endpointUrl('questionnaireUserExport')
      .replace('<name>', name)
      .replace('<user_id>', user_id);
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

  /** search */
  search(query: Query): Observable<Query> {
    const url = this._endpointUrl('search');
    return this.httpClient.post<Query>(url, query)
      .pipe(catchError(this._handleError));
  }

  /** getDataTransferLogs */
  getDataTransferLogs(pageNumber = 0, pageSize = 10): Observable<DataTransferPageResults> {
    const search_data = {pageNumber: String(pageNumber), pageSize: String(pageSize)};
    return this.httpClient.get<DataTransferPageResults>(this._endpointUrl('data_transfer_log'), {params: search_data})
      .pipe(catchError(this._handleError));
  }

  /** getZipCoords */
  getZipCoords(zipCode: string): Observable<GeoLocation> {
    const url = this._endpointUrl('zip_code_coords')
      .replace('<id>', zipCode);
    return this.httpClient.get<any>(url)
      .pipe(catchError(this._handleError));
  }

  private _handleError(error: StarError) {
    let message = 'Could not complete your request; please try again later.';
    message = error.message;
    // return an observable with a user-facing error message
    return throwError(message);
  }

  private setServerStatus() {
    this.httpClient.get<Status>(this._endpointUrl('status')).subscribe
    (status => {
      this.statusSubject.next(status);
    });
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
