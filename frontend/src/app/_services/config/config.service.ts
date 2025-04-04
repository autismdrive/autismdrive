import {HttpClient} from '@angular/common/http';
import {Injectable, signal, WritableSignal} from '@angular/core';
import {environment} from '@environments/environment';
import {ConfigServiceProps} from '@models/config-service-props';
import {GoogleModuleOptions} from '@ng-maps/google';
import {lastValueFrom} from 'rxjs';

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

  constructor(private httpClient: HttpClient) {
    this.load();
  }

  async load() {
    let configFromJsonFile: ConfigServiceProps;

    // Check if a file called `config.json` is available in this file's directory.
    // If it is, load the configuration from there.
    try {
      configFromJsonFile = await lastValueFrom(
        this.httpClient.get<ConfigServiceProps>('/assets/config.json', {responseType: 'json'}),
      );
    } catch {
      configFromJsonFile = undefined;
    }

    if (configFromJsonFile) {
      this.fromProperties(configFromJsonFile);
      return;
    }

    // Check with the backend to see if there is a configuration override available.
    const backendConfigEndpoint = `${environment.api}/api/config`;
    let configFromBackend: ConfigServiceProps;
    try {
      configFromBackend = await lastValueFrom(
        this.httpClient.get<ConfigServiceProps>(backendConfigEndpoint, {responseType: 'json'}),
      );
    } catch {
      configFromBackend = undefined;
    }

    if (configFromBackend) {
      this.fromProperties(configFromBackend);
      return;
    }
  }

  fromProperties(props: ConfigServiceProps) {
    const instance = this;
    Object.entries(props).forEach(([key, value]) => {
      instance[key] = value;
    });

    this.props.set(props);
  }
}
