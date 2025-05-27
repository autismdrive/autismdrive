import {AbstractControl, ValidationErrors} from '@angular/forms';

export function ValidatePasswordsMatch(control: AbstractControl): ValidationErrors {
  // Verifies that this field matches a field on the same form called "password".
  const dataForm = control.parent;
  if (!dataForm) {
    return null;
  }

  const password = dataForm.get('password').value;
  const passwordRepeated = control.value;

  if (password !== passwordRepeated) {
    /* for newPasswordRepeat from current field "newPassword" */
    const error: ValidationErrors = {MatchPassword: true};
    return error;
  } else {
    return null;
  }
}
