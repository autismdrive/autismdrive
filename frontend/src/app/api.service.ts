import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { Study } from './study';
import { Resource } from './resource';
import { Training } from './training';

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
  };

  constructor(private httpClient: HttpClient) {
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
