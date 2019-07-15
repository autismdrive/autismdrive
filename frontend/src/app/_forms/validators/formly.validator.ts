import { FormControl, ValidationErrors } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
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
  return URL_REGEX.test(control.value) ? null : { 'url': true };
}

export function UrlValidatorMessage(err, field: FormlyFieldConfig) {
  return `We cannot save "${field.formControl.value}". Please provide the full path, including http:// or https://`;
}

export function PhoneValidator(control: FormControl): ValidationErrors {
  return PHONE_REGEX.test(control.value) ? null : { 'phone': true };
}

export function PhoneValidatorMessage(err, field: FormlyFieldConfig) {
  return `"${field.formControl.value}" is not a valid phone number`;
}
