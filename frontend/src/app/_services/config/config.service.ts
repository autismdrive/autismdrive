import {effect, Injectable, signal, Signal, WritableSignal} from '@angular/core';
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

  public readonly props: WritableSignal<ConfigServiceProps | undefined> = signal(undefined);

  constructor() {
    effect(() => {
      const value = this.props();

      console.log('ConfigService > constructor > effect > value', value);
    });
  }

  fromProperties(props: ConfigServiceProps) {
    const instance = this;
    Object.entries(props).forEach(([key, value]) => {
      instance[key] = value;
    });

    this.props.set(props);
  }
}
