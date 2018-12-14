import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  ErrorStateMatcher,
  MatCardModule,
  MatFormFieldModule,
  MatInputModule,
  MatSelectModule
} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ColorPickerModule } from 'ngx-color-picker';
import { MarkdownModule } from 'ngx-markdown';
import { SDFormField } from '../form-field';
import { MockApiService } from '../../testing/mocks/api.service.mock';
import { ApiService } from '../../api.service';
import { SDFormFieldComponent } from './form-field.component';

describe('FormFieldComponent', () => {
  let api: MockApiService;
  let component: SDFormFieldComponent;
  let errorMatcher: ErrorStateMatcher;
  let fixture: ComponentFixture<SDFormFieldComponent>;

  beforeEach(async(() => {
    api = new MockApiService();
    errorMatcher = new ErrorStateMatcher();

    TestBed
      .configureTestingModule({
        declarations: [
          SDFormFieldComponent
        ],
        imports: [
          BrowserAnimationsModule,
          ColorPickerModule,
          FormsModule,
          MarkdownModule,
          MatCardModule,
          MatFormFieldModule,
          MatInputModule,
          MatSelectModule,
          ReactiveFormsModule
        ],
        providers: [
          { provide: ApiService, useValue: api },
          { provide: ErrorStateMatcher, useValue: { isErrorState: () => true } }
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(SDFormFieldComponent);
        component = fixture.componentInstance;
        component.errorMatcher = errorMatcher;
        component.field = new SDFormField({
          formControl: new FormControl(),
          required: false,
          placeholder: 'Beep boop boop beeee?',
          type: 'text'
        });
        fixture.detectChanges();
      });
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
