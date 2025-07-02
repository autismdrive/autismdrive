import {ParamMap} from '@angular/router';

/**
 * Returns true if the two given maps have the same keys and values, false otherwise.
 */
export const paramMapsAreEqual = (a: ParamMap, b: ParamMap): boolean => {
  const isParamMap = (map: any): map is ParamMap => {
    return map && typeof map.keys === 'function' && typeof map.get === 'function' && typeof map.has === 'function';
  };

  if (!isParamMap(a) || !isParamMap(b)) {
    return true;
  }

  return a.keys.every(k => b.has(k) && a.get(k) === b.get(k)) && b.keys.every(k => a.has(k) && b.get(k) === a.get(k));
};
