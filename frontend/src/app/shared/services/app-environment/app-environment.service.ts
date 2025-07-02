import {Injectable, signal, WritableSignal} from '@angular/core';
import {AppEnvironment} from '@app/shared/models/environment';
import {GoogleMapsMapIds} from '@models/google-maps-api-config';

@Injectable({
  providedIn: 'root',
})
export class AppEnvironmentService implements AppEnvironment {
  development: boolean;
  testing: boolean;
  mirroring: boolean;
  production: boolean;
  apiUrl: string;
  googleAnalyticsTagId: string;
  googleMapsApiKey: string;
  googleMapsMapIds: GoogleMapsMapIds;

  public readonly props: WritableSignal<AppEnvironment | undefined> = signal(undefined);

  constructor() {}

  fromProperties(props: AppEnvironment) {
    const instance = this;
    Object.entries(props).forEach(([key, value]) => {
      instance[key] = value;
    });

    this.props.set(props);
  }
}
