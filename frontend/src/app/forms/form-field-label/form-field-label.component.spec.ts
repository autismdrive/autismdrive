import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FormField } from '../form-field';
import { FormFieldLabelComponent } from './form-field-label.component';

describe('FormFieldLabelComponent', () => {
  let component: FormFieldLabelComponent;
  let fixture: ComponentFixture<FormFieldLabelComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        declarations: [FormFieldLabelComponent],
        imports: [
          FormsModule,
          ReactiveFormsModule
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(FormFieldLabelComponent);
        component = fixture.componentInstance;
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
