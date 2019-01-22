import { FormlyFieldConfig } from '@ngx-formly/core';

export class QuestionnaireStep {
  label: string;
  description: string;
  fields: FormlyFieldConfig[];

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
