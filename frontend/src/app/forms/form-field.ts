import { FormControl, FormGroup } from '@angular/forms';
import { SDFileAttachment } from './file-attachment';

export class SDFormField {
  fieldsetId?: string;
  fieldsetLabel?: string;
  formControl?: FormControl;
  formGroup?: FormGroup;
  helpText?: string;
  maxLength?: number;
  minLength?: number;
  multiSelect = false;
  options?: object;
  placeholder: string;
  required?: boolean;
  showIcons = false;
  type: string;
  passwordsMatch?: boolean;

  // 'files' type
  attachments = new Map<string, SDFileAttachment>();

  // 'select' type can pull from a hard-coded list
  // or from API. If selectOptions is not provided,
  // apiSource will be used.
  selectOptions?: string[];
  apiSource?: string; // Should be the name of the API function to call

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}

