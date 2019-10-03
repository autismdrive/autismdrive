import { FormControl, ValidationErrors } from '@angular/forms';
import {FieldType, FormlyFieldConfig} from '@ngx-formly/core';
import EMAIL_REGEX from './email.regex';
import PHONE_REGEX from './phone.regex';
import URL_REGEX from './url.regex';

export function EmailValidator(control: FormControl): ValidationErrors {
  return EMAIL_REGEX.test(control.value) ? null : { 'email': true };
}

export function EmailValidatorMessage(err, field: FormlyFieldConfig) {
  return `"${field.formControl.value}" is not a valid email address`;
}

export function UrlValidator(control: FormControl): ValidationErrors {
  return  !control.value || URL_REGEX.test(control.value) ? null : { 'url': true };
}

export function UrlValidatorMessage(err, field: FormlyFieldConfig) {
  return `We cannot save "${field.formControl.value}". Please provide the full path, including http:// or https://`;
}

export function PhoneValidator(control: FormControl): ValidationErrors {
  return  !control.value || PHONE_REGEX.test(control.value) ? null : { 'phone': true };
}

export function PhoneValidatorMessage(err, field: FormlyFieldConfig) {
  return `"${field.formControl.value}" is not a valid phone number`;
}

export function MulticheckboxValidator(control: FormControl): ValidationErrors {
  if (control.value) {
    for (const key in control.value) {
      if (control.value[key] === true) {
        return null;
      }
    }
  }
  return { required: true };
}

export function MulticheckboxValidatorMessage(err, field: FormlyFieldConfig) {
  return 'At least one of these checkboxes must be selected.';
}

export function MinValidationMessage(err, field) {
  return `This value should be more than ${field.templateOptions.min}`;
}

export function MaxValidationMessage(err, field) {
  return `This value should be less than ${field.templateOptions.max}`;
}

export function ShowError(field: FieldType) {
  return field.formControl &&
    field.formControl.invalid &&
    (
      field.formControl.dirty ||
      (field.options.parentForm && field.options.parentForm.submitted) ||
      (field.field.validation && field.field.validation.show)
    );
}
