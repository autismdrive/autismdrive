import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SDFileUploadComponent } from './file-upload.component';
import { MatTableModule } from '@angular/material';
import { ApiService } from '../../api.service';
import { MockApiService } from '../../testing/mocks/api.service.mock';
import { ReactiveFormsModule, FormsModule, FormControl } from '@angular/forms';
import { SDFormField } from '../form-field';
import { SDFileAttachment } from '../file-attachment';

describe('SDFileUploadComponent', () => {
  let component: SDFileUploadComponent;
  let fixture: ComponentFixture<SDFileUploadComponent>;
  let api: MockApiService;

  beforeEach(async(() => {
    api = new MockApiService();

    TestBed
      .configureTestingModule({
        declarations: [SDFileUploadComponent],
        imports: [
          FormsModule,
          MatTableModule,
          ReactiveFormsModule
        ],
        providers: [
          { provide: ApiService, useValue: api }
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(SDFileUploadComponent);
        component = fixture.componentInstance;
        component.field = new SDFormField({
          formControl: new FormControl(),
          attachments: new Map<number | string, SDFileAttachment>(),
          required: false,
          placeholder: 'Attachments',
          type: 'files'
        });
        fixture.detectChanges();
      });
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
