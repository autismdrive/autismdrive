import { ChangeDetectionStrategy, Component, Input, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FormGroup, ValidationErrors } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material';
import { SDFormField } from '../form-field';
import { SDFormSelectOption } from '../form-select-option';
import { ApiService } from '../../api.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-form-field',
  templateUrl: './form-field.component.html',
  styleUrls: ['./form-field.component.scss']
})
export class SDFormFieldComponent implements OnInit {
  @Input() field: SDFormField;
  @Input() errors: ValidationErrors;
  @Input() errorMatcher: ErrorStateMatcher;
  @Input() formGroup: FormGroup;
  options = [];
  dataLoaded = false;

  constructor(private api: ApiService) {
  }

  ngOnInit() {
    this.loadOptions();
  }

  loadOptions() {
    if (this.field.type === 'select') {
      if (this.field.hasOwnProperty('selectOptions')) {
        this.options = this.field.selectOptions.map(s => new SDFormSelectOption({ id: s, name: s }));
        this.dataLoaded = true;
      } else if (this.field.hasOwnProperty('apiSource')) {
        const source = this.field.apiSource;

        if (this.api[source] && (typeof this.api[source] === 'function')) {
          this.api[source]().subscribe(results => {
            this.options = results;
            this.field.formControl.updateValueAndValidity();
            this.dataLoaded = true;
          });
        }
      }
    } else {
      this.dataLoaded = true;
    }
  }

  currentLength() {
    return (
      this.field &&
      this.field.formControl &&
      this.field.formControl.value &&
      this.field.formControl.value.length
    ) || 0;
  }

  // Replaces underscores with spaces and capitalizes each word in given string
  getLabel(s) {
    return s.split('_').map(w => w[0].toUpperCase() + w.substr(1)).join(' ');
  }

  isTextField(field: SDFormField) {
    return ['text', 'url', 'email', 'password'].indexOf(field.type) > -1;
  }

  isNormalField(field: SDFormField) {
    return !(['tree', 'richtexteditor', 'toggle', 'files', 'checkbox'].indexOf(field.type) > -1);
  }
}

