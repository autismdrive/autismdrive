import {HttpClient} from '@angular/common/http';
import {Injectable, signal, WritableSignal} from '@angular/core';
import {environment} from '@environments/environment';
import {AppEnvironment} from '@models/environment';
import {lastValueFrom} from 'rxjs';

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
  googleTagManagerId: string;
  googleMapsApiKey: string;

  public readonly props: WritableSignal<AppEnvironment | undefined> = signal(undefined);

  constructor(private httpClient: HttpClient) {
  }

  async load() {
    let configFromJsonFile: AppEnvironment;

    // Check if a file called `config.json` is available in this file's directory.
    // If it is, load the configuration from there.
    try {
      configFromJsonFile = await lastValueFrom(
        this.httpClient.get<AppEnvironment>('/assets/config.json', {responseType: 'json'}),
      );
    } catch {
      configFromJsonFile = undefined;
    }

    if (configFromJsonFile) {
      this.fromProperties(configFromJsonFile);
      return;
    }

    // Check with the backend to see if there is a configuration override available.
    const backendConfigEndpoint = `${environment.apiUrl}/api/config`;
    let configFromBackend: AppEnvironment;
    try {
      configFromBackend = await lastValueFrom(
        this.httpClient.get<AppEnvironment>(backendConfigEndpoint, {responseType: 'json'}),
      );
    } catch {
      configFromBackend = undefined;
    }

    if (configFromBackend) {
      this.fromProperties(configFromBackend);
      return;
    }
  }

  fromProperties(props: AppEnvironment) {
    const instance = this;
    Object.entries(props).forEach(([key, value]) => {
      instance[key] = value;
    });

    this.props.set(props);
  }
}
