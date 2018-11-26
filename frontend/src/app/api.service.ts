import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { Resource } from './interfaces';

@Injectable()
export class ApiService {

  apiRoot = environment.api;

  // REST endpoints
  endpoints = {
    resourceList: '/api/resource',
    resource: '/api/resource/<id>',
  };

  constructor(private httpClient: HttpClient) {
  }

  // Add Resource
  addResource(resource: any): Observable<any> {
    console.log('adding a resource:', resource);
    return this.httpClient.post<any>(this.apiRoot + this.endpoints.resourceList, resource)
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
