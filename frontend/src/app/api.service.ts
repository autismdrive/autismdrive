import {
  HttpClient,
  HttpErrorResponse,
  HttpEvent,
  HttpEventType,
  HttpHeaders,
  HttpParams
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { NgProgress } from 'ngx-progressbar';
import { Observable, throwError } from 'rxjs';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';
import { catchError, last, map } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { SDFileAttachment } from './forms/file-attachment';
import { Resource } from './resource';
import { Study } from './study';
import { Training } from './training';
import { User } from './user';

@Injectable()
export class ApiService {

  apiRoot = environment.api;

  // REST endpoints
  endpoints = {
    fileAttachment: '/api/file/<file_id>', // One file
    fileAttachmentList: '/api/file', // All files
    forgot_password: '/api/forgot_password',
    login_password: '/api/login_password',
    reset_password: '/api/reset_password',
    resource: '/api/resource/<id>',
    resourceList: '/api/resource',
    session: '/api/session',
    study: '/api/study/<id>',
    studyList: '/api/study',
    training: '/api/training/<id>',
    trainingList: '/api/training',
    userList: '/api/user',
    contactQuestionnaireList: '/api/contact_questionnaire',
    contactQuestionnaire: '/api/contact_questionnaire/<id>',
    contactQuestionnaireMeta: '/api/contact_questionnaire/meta',
    demographicsQuestionnaireList: '/api/demographics_questionnaire',
    demographicsQuestionnaire: '/api/demographics_questionnaire/<id>',
    guardianDemographicsQuestionnaireList: '/api/guardian_demographics_questionnaire',
    guardianDemographicsQuestionnaire: '/api/guardian_demographics_questionnaire/<id>',
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

  /** Update Study */
  updateStudy(study: Study): Observable<Study> {
    console.log('updating a study:', study);
    return this.httpClient.put<Study>(`${this.apiRoot + this.endpoints.study}/${study.id}`, study)
      .pipe(catchError(this.handleError));
  }

  /** Delete Study */
  deleteStudy(study: Study): Observable<Study> {
    console.log('deleting a study:', study);
    return this.httpClient.delete<Study>(`${this.apiRoot + this.endpoints.study}/${study.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Study */
  getStudy(id: number): Observable<Study> {
    console.log('getting Study number ', id);
    return this.httpClient.get<Study>(this.apiRoot + this.endpoints.study.replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Studies */
  getStudies(): Observable<Study[]> {
    console.log('getting a list of Studies');
    return this.httpClient.get<Study[]>(this.apiRoot + this.endpoints.studyList)
      .pipe(catchError(this.handleError));
  }

  /** Add Resource */
  addResource(resource: Resource): Observable<Resource> {
    console.log('adding a resource:', resource);
    return this.httpClient.post<Resource>(this.apiRoot + this.endpoints.resourceList, resource)
      .pipe(catchError(this.handleError));
  }

  /** Update resource */
  updateResource(resource: Resource): Observable<Resource> {
    console.log('updating a resource:', resource);
    return this.httpClient.put<Resource>(`${this.apiRoot + this.endpoints.resource}/${resource.id}`, resource)
      .pipe(catchError(this.handleError));
  }

  /** Delete Resource */
  deleteResource(resource: Resource): Observable<Resource> {
    console.log('deleting a resource:', resource);
    return this.httpClient.delete<Resource>(`${this.apiRoot + this.endpoints.resource}/${resource.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Resource */
  getResource(id: number): Observable<Resource> {
    console.log('getting resource number ', id);
    return this.httpClient.get<Resource>(this.apiRoot + this.endpoints.resource.replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Resources */
  getResources(): Observable<Resource[]> {
    console.log('getting a list of resources');
    return this.httpClient.get<Resource[]>(this.apiRoot + this.endpoints.resourceList)
      .pipe(catchError(this.handleError));
  }

  /** Add Training */
  addTraining(training: Training): Observable<Training> {
    console.log('adding a training:', training);
    return this.httpClient.post<Training>(this.apiRoot + this.endpoints.trainingList, training)
      .pipe(catchError(this.handleError));
  }

  /** Update Training */
  updateTraining(training: Training): Observable<Training> {
    console.log('updating a training:', training);
    return this.httpClient.put<Training>(`${this.apiRoot + this.endpoints.training}/${training.id}`, training)
      .pipe(catchError(this.handleError));
  }

  /** Delete Training */
  deleteTraining(training: Training): Observable<Training> {
    console.log('deleting a training:', training);
    return this.httpClient.delete<Training>(`${this.apiRoot + this.endpoints.training}/${training.id}`)
      .pipe(catchError(this.handleError));
  }

  /** Get Training */
  getTraining(id: number): Observable<Training> {
    console.log('getting training number ', id);
    return this.httpClient.get<Training>(this.apiRoot + this.endpoints.training.replace('<id>', id.toString()))
      .pipe(catchError(this.handleError));
  }

  /** Get Trainings */
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

  /** showProgress
   * Return distinct message for sent, upload progress, & response events */
  private showProgress(event: HttpEvent<any>, attachment: SDFileAttachment, progress: NgProgress): SDFileAttachment {
    switch (event.type) {
      case HttpEventType.Sent:
        progress.start();
        break;
      case HttpEventType.UploadProgress:
        progress.set(Math.round(100 * event.loaded / event.total));
        break;
      case HttpEventType.DownloadProgress:
        progress.set(Math.round(100 * event.loaded / event.total));
        break;
      case HttpEventType.Response:
        progress.done();
        return attachment;
      default:
        break;
    }
  }


  /** getFileAttachment */
  getFileAttachment(id?: number, md5?: string): Observable<SDFileAttachment> {
    const params = { id: String(id), md5: md5 };
    const url = this.apiRoot + this.endpoints.fileAttachmentList;

    return this.httpClient.get<SDFileAttachment>(url, { params: params });
  }

  /** updateFileAttachment */
  updateFileAttachment(attachment: SDFileAttachment): Observable<SDFileAttachment> {
    const url = this.endpoints.fileAttachment.replace('<file_id>', attachment.id.toString());
    const attachmentMetadata = {
      display_name: attachment.display_name,
      date_modified: new Date(attachment.lastModified || attachment.date_modified),
      md5: attachment.md5,
      mime_type: attachment.type || attachment.mime_type,
      size: attachment.size,
      resource_id: attachment.resource_id
    };

    return this.httpClient.put<SDFileAttachment>(this.apiRoot + url, attachmentMetadata)
      .pipe(catchError(this.handleError));
  }

  /** getFileAttachmentBlob*/
  getFileAttachmentBlob(attachment: SDFileAttachment): Observable<Blob> {
    const options: {
      headers?: HttpHeaders,
      observe?: 'body',
      params?: HttpParams,
      reportProgress?: boolean,
      responseType: 'json',
      withCredentials?: boolean,
    } = {
      responseType: 'blob' as 'json'
    };

    return this.httpClient.get<Blob>(attachment.url, options)
      .pipe(catchError(this.handleError));
  }

  /** deleteFileAttachment */
  deleteFileAttachment(attachment: SDFileAttachment): Observable<SDFileAttachment> {
    const url = this.endpoints.fileAttachment.replace('<file_id>', attachment.id.toString());
    return this.httpClient.delete<SDFileAttachment>(this.apiRoot + url)
      .pipe(catchError(this.handleError));
  }

  /** addFileAttachment */
  addFileAttachment(attachment: SDFileAttachment): Observable<SDFileAttachment> {
    const url = this.apiRoot + this.endpoints.fileAttachmentList;
    const attachmentMetadata = {
      file_name: attachment.name,
      display_name: attachment.name,
      date_modified: new Date(attachment.lastModified),
      md5: attachment.md5,
      mime_type: attachment.type,
      size: attachment.size
    };

    return this.httpClient.post<SDFileAttachment>(url, attachmentMetadata)
      .pipe(catchError(this.handleError));
  }

  /** addFileAttachmentBlob */
  addFileAttachmentBlob(attachmentId: number, attachment: SDFileAttachment, progress: NgProgress): Observable<SDFileAttachment> {
    const url = this.endpoints.fileAttachment.replace('<file_id>', attachmentId.toString());
    const options: {
      headers?: HttpHeaders,
      observe: 'events',
      params?: HttpParams,
      reportProgress?: boolean,
      responseType: 'json',
      withCredentials?: boolean
    } = {
      observe: 'events',
      reportProgress: true,
      responseType: 'blob' as 'json'
    };

    return this.httpClient.put<File>(this.apiRoot + url, attachment, options)
      .pipe(
        map(event => this.showProgress(event, attachment, progress)),
        last(), // return last (completed) message to caller
        catchError(this.handleError)
      );
  }

  /** getQuestionnaire */
  getQuestionnaire(key: string, id: number) {
    const path = this.endpoints[key + 'Questionnaire'].replace('<id>', id.toString());
    return this.httpClient.get<any>(this.apiRoot + path)
      .pipe(catchError(this.handleError));
  }

  /** updateQuestionnaire */
  updateQuestionnaire(key: string, id: number, options: object) {
    const path = this.endpoints[key + 'Questionnaire'].replace('<id>', id.toString());
    return this.httpClient.post<object>(this.apiRoot + path, options)
      .pipe(catchError(this.handleError));
  }

  /** getQuestionnaireMeta */
  getQuestionnaireMeta(key: string) {
    const path = this.endpoints[key + 'QuestionnaireMeta'];
    return this.httpClient.get<any>(this.apiRoot + path)
      .pipe(catchError(this.handleError));
  }

  /** getQuestionnaireList */
  getQuestionnaireList(key: string) {
    const path = this.endpoints[key + 'QuestionnaireList'];
    return this.httpClient.get<any>(this.apiRoot + path)
      .pipe(catchError(this.handleError));
  }

  /** submitQuestionnaire */
  submitQuestionnaire(key: string, options: object) {
    const path = this.endpoints[key + 'QuestionnaireList'];
    return this.httpClient.post<object>(this.apiRoot + path, options)
      .pipe(catchError(this.handleError));
  }

}
