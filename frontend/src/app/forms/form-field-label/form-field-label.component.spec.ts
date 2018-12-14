import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SDFormField } from '../form-field';
import { SDFormFieldLabelComponent } from './form-field-label.component';

describe('FormFieldLabelComponent', () => {
  let component: SDFormFieldLabelComponent;
  let fixture: ComponentFixture<SDFormFieldLabelComponent>;

  beforeEach(async(() => {
    TestBed
      .configureTestingModule({
        declarations: [SDFormFieldLabelComponent],
        imports: [
          FormsModule,
          ReactiveFormsModule
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(SDFormFieldLabelComponent);
        component = fixture.componentInstance;
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
