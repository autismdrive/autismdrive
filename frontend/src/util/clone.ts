import {Observable} from 'rxjs';
import {AbstractControl} from '@angular/forms';

export const isNullOrUndefined = function (value: any) {
  return value === undefined || value === null;
}

export const isObject = function (x: any) {
  return x != null && typeof x === 'object';
}

export const clone = function (value: any): any {
  if (!isObject(value) || value instanceof RegExp || value instanceof Observable || /* instanceof SafeHtmlImpl */ value.changingThisBreaksApplicationSecurity) {
    return value;
  }

  if (value instanceof AbstractControl) {
    return null;
  }

  if (value instanceof Date) {
    return new Date(value.getTime());
  }

  if (Array.isArray(value)) {
    return value.slice(0).map(v => clone(v));
  }

  value = Object.assign({}, value);
  Object.keys(value).forEach(k => value[k] = clone(value[k]));

  return value;
}
