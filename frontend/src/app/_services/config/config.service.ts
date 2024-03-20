import {LazyMapsAPILoaderConfigLiteral} from '@agm/core';
import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ConfigService implements LazyMapsAPILoaderConfigLiteral {
  public apiUrl: string;
  public apiKey: string; // The google maps api key, to implement LazyMapsAPI
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
