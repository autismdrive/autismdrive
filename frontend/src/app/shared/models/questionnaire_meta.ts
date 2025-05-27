import {FormlyFieldConfig} from '@ngx-formly/core';
import {CamelCasedPropertiesDeep, SnakeCasedPropertiesDeep} from 'type-fest';

export interface CustomFieldConfigSnakeCase {
  display_order?: number;
  repeat_class?: number;
}

export type FormlyFieldConfigSnakeCase = SnakeCasedPropertiesDeep<FormlyFieldConfig>;
export type FieldConfigSnakeCase = FormlyFieldConfigSnakeCase & CustomFieldConfigSnakeCase;
export type CustomFieldConfigCamelCase = CamelCasedPropertiesDeep<CustomFieldConfigSnakeCase>;
export type FieldConfigCamelCase = FormlyFieldConfig & CustomFieldConfigCamelCase;

export interface QuestionnaireMeta {
  table: {
    question_type: string;
    label: string;
  };
  fields: FieldConfigSnakeCase[];
}
