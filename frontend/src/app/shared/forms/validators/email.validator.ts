import {AbstractControl, ValidationErrors} from '@angular/forms';
import EMAIL_REGEX from './email.regex';

export function ValidateEmail(control: AbstractControl): ValidationErrors {
  if (!EMAIL_REGEX.test(control.value) && control.value && control.value !== '') {
    return {url: true};
  }

  return null;
}
