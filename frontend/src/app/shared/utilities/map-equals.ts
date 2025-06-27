import {ParamMap} from '@angular/router';

/**
 * Returns true if the two given maps have the same keys and values, false otherwise.
 */
export const paramMapsAreEqual = (a: ParamMap, b: ParamMap): boolean => {
  return a.keys.every(k => b.has(k) && a.get(k) === b.get(k)) && b.keys.every(k => a.has(k) && b.get(k) === a.get(k));
};
