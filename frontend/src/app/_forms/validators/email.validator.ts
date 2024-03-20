import {AbstractControl, ValidationErrors} from '@angular/forms';
import EMAIL_REGEX from './email.regex';

export function ValidateEmail(control: AbstractControl): ValidationErrors {
  if (!EMAIL_REGEX.test(control.value) && control.value && control.value !== '') {
    const error: ValidationErrors = {url: true};
    return error;
  }
}
