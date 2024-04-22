import {GoogleModuleOptions} from '@ng-maps/google';
import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ConfigService implements GoogleModuleOptions {
  public apiUrl: string;
  public apiKey: string; // The Google Maps api key, to implement GoogleModuleOptions
  public development: boolean;
  public testing: boolean;
  public mirroring: boolean;
  public production: boolean;
  public googleAnalyticsKey: string;

  fromProperties(props) {
    for (const propName in props) {
      if (props.hasOwnProperty(propName)) {
        this[propName] = props[propName];
      }
    }
  }
}
