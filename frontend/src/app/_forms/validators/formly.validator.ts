import { FormControl, ValidationErrors } from '@angular/forms';
import { FormlyFieldConfig } from '@ngx-formly/core';
import EMAIL_REGEX from './email.regex';
import PHONE_REGEX from './phone.regex';

export function EmailValidator(control: FormControl): ValidationErrors {
  return EMAIL_REGEX.test(control.value) ? null : { 'email': true };
}

export function EmailValidatorMessage(err, field: FormlyFieldConfig) {
  return `"${field.formControl.value}" is not a valid email address`;
}

export function PhoneValidator(control: FormControl): ValidationErrors {
  return PHONE_REGEX.test(control.value) ? null : { 'phone': true };
}

export function PhoneValidatorMessage(err, field: FormlyFieldConfig) {
  return `"${field.formControl.value}" is not a valid phone number`;
}
