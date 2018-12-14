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
import { FormField } from '../form-field';
import { MockResourceApiService } from '../shared/mocks/resource-api.service.mock';
import { ResourceApiService } from '../shared/resource-api/resource-api.service';
import { FormFieldComponent } from './form-field.component';

describe('FormFieldComponent', () => {
  let api: MockResourceApiService;
  let component: FormFieldComponent;
  let errorMatcher: ErrorStateMatcher;
  let fixture: ComponentFixture<FormFieldComponent>;

  beforeEach(async(() => {
    api = new MockResourceApiService();
    errorMatcher = new ErrorStateMatcher();

    TestBed
      .configureTestingModule({
        declarations: [
          FormFieldComponent
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
          { provide: ResourceApiService, useValue: api },
          { provide: ErrorStateMatcher, useValue: { isErrorState: () => true } }
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(FormFieldComponent);
        component = fixture.componentInstance;
        component.errorMatcher = errorMatcher;
        component.field = new FormField({
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
