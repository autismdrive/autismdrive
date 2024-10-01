import {HttpHeaders, HttpResponse} from '@angular/common/http';

export const mockExportResponse = new HttpResponse<Blob>({
  headers: new HttpHeaders({'x-filename': 'test.csv'}),
  body: new Blob(['test']),
});
