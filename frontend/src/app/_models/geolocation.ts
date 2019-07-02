import { getDistance, convertDistance } from 'geolib';
import { UserInputCoordinates } from 'geolib/es/types';

export class GeoLocation {
  latitude?: number;
  longitude?: number;

  constructor(private _superprops) {
    for (const propName in this._superprops) {
      if (this._superprops.hasOwnProperty(propName)) {
        this[propName] = this._superprops[propName];
      }
    }
  }

  hasCoords(): boolean {
    const _isSet = n => (typeof n === 'number') && isFinite(n);
    return (_isSet(this.latitude) && _isSet(this.longitude));
  }

  milesFrom(there: UserInputCoordinates) {
    if (there && this.hasCoords()) {
      const here: UserInputCoordinates = {lat: this.latitude, lng: this.longitude};
      const dist = getDistance(here, there);
      return convertDistance(dist, 'mi').toFixed(1);
    }
  }
}
