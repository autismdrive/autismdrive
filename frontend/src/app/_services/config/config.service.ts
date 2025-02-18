import {Injectable} from '@angular/core';
import {GoogleModuleOptions} from '@ng-maps/google';
import {BehaviorSubject, Observable} from 'rxjs';

export interface ConfigServiceProps {
  apiUrl: string;
  apiKey: string;
  development: boolean;
  testing: boolean;
  mirroring: boolean;
  production: boolean;
  googleAnalyticsKey: string;
}

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

  private propsSubject = new BehaviorSubject<ConfigServiceProps>(null);
  public props: Observable<ConfigServiceProps>;

  constructor() {
    this.props = this.propsSubject.asObservable();
    this.propsSubject.next(null);
  }

  fromProperties(props: ConfigServiceProps) {
    for (const propName in props) {
      if (props.hasOwnProperty(propName)) {
        this[propName] = props[propName];
      }
    }

    this.propsSubject.next(props);
  }
}
