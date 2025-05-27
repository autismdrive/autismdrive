/// <reference types="@types/google.maps" />
import {DOCUMENT} from '@angular/common';
import {effect, Inject, Injectable, Renderer2, signal, WritableSignal} from '@angular/core';
import {GoogleMapsAPIWrapper, GoogleModuleOptions} from '@ng-maps/google';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';

declare let google;

@Injectable({
  providedIn: 'root',
})
export class GoogleMapsLibraryService {
  public readonly options: WritableSignal<GoogleModuleOptions | undefined> = signal(undefined);
  public readonly core: WritableSignal<google.maps.CoreLibrary | undefined> = signal(undefined);

  constructor(
    private appEnvironmentService: AppEnvironmentService,
    private googleMapsAPIWrapper: GoogleMapsAPIWrapper,
  ) {
    console.log(
      'GoogleMapsLibraryService > constructor > appEnvironmentService.googleMapsApiKey:',
      this.appEnvironmentService.googleMapsApiKey,
    );
  }

  set googleModuleOptions(value: GoogleModuleOptions) {
    this.options.set(value);
  }

  get googleModuleOptions(): GoogleModuleOptions {
    return this.options();
  }

  async load() {
    this.googleMapsAPIWrapper['_loader'].configure(this.options());

    await google?.maps?.importLibrary('core').then(result => {
      this.core.set(result as google.maps.CoreLibrary);
    });
  }
}
