import {FormlyFieldConfig} from '@ngx-formly/core';

export interface RepeatSectionDialogData {
  title: string;
  fields: FormlyFieldConfig[];
  model?: any;
}
