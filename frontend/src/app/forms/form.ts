import { ValidatePasswordsMatch } from './validators/password_match.validator';
import { FormGroup, Validators } from '@angular/forms';
import { SDFormField } from './form-field';

export class SDForm {

  constructor(private fields: SDFormField[], private form: FormGroup) { }

  getFields(): SDFormField[] {
    const fields = [];

    for (const fieldName in this.fields) {
      if (this.fields.hasOwnProperty(fieldName)) {
        fields.push(this.fields[fieldName]);
      }
    }
    return fields;
  }

  loadForm() {
    for (const fieldName in this.fields) {
      if (this.fields.hasOwnProperty(fieldName)) {
        const field = this.fields[fieldName];
        const validators = [];

        if (field.required) {
          validators.push(Validators.required);
        }

        if (field.minLength) {
          validators.push(Validators.minLength(field.minLength));
        }

        if (field.maxLength) {
          validators.push(Validators.maxLength(field.maxLength));
        }

        if (field.type === 'email') {
          validators.push(Validators.email);
        }

        if (field.passwordsMatch) {
          validators.push(ValidatePasswordsMatch);
        }

        field.formControl.setValidators(validators);
        this.form.addControl(fieldName, field.formControl);
      }
    }
  }

  setObjectToEdit(object: any) {
    for (const fieldName in this.fields) {
      if (this.fields.hasOwnProperty(fieldName)) {
        const field = this.fields[fieldName];
        field.formControl.patchValue(object[fieldName]);
      }
    }
  }

  updateObject(object: any) {
    for (const fieldName in this.fields) {
      if (this.fields.hasOwnProperty(fieldName)) {
        const field = this.fields[fieldName];
        object[fieldName] = field.formControl.value;
      }
    }
  }

  validate() {
    for (const key in this.form.controls) {
      if (this.form.controls.hasOwnProperty(key)) {
        const control = this.form.controls[key];
        control.markAsTouched();
        control.updateValueAndValidity();
      }
    }
  }

}
