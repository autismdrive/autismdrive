import { Component, OnInit, Input } from '@angular/core';
import { SDFormField } from '../form-field';
import { ValidationErrors } from '@angular/forms';

@Component({
  selector: 'app-form-field-label',
  templateUrl: './form-field-label.component.html',
  styleUrls: ['./form-field-label.component.scss']
})
export class SDFormFieldLabelComponent implements OnInit {
  @Input() field: SDFormField;
  @Input() errors: ValidationErrors;

  constructor() { }

  ngOnInit() {
  }

  isValid(field: SDFormField) {
    if (field.formControl) {
      return field.formControl.valid;
    } else if (field.formGroup) {
      return field.formGroup.valid;
    } else {
      return true;
    }
  }
}

