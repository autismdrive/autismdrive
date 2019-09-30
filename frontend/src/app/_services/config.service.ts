import {Injectable} from '@angular/core';
import {LazyMapsAPILoaderConfigLiteral} from '@agm/core';

@Injectable({
  providedIn: 'root'
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

/*
# Base ---
export const environment = {
  production: false,
  api: `http://${localhost}:5000`,
  gc_api_key: '',
  googleAnalyticsKey: 'UA-145661791-1'
};

# Mirroring ---
export const environment = {
  production: false,
  api: `http://${localhost}:5001`,
  gc_api_key: 'API_KEY_GOES_HERE',
  googleAnalyticsKey: 'UA-145661791-1'
};

# Staging ---
export const environment = {
  production: false,
  api: `http://${localhost}:5000`,
  gc_api_key: 'API_KEY_GOES_HERE',
  googleAnalyticsKey: 'UA-145661791-1'
};
*/
