/// <reference types="@types/google.maps" />
import {isPlatformBrowser, isPlatformServer} from '@angular/common';
import {afterNextRender, effect, Inject, Injectable, NgZone, PLATFORM_ID, signal, WritableSignal} from '@angular/core';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';
import {GoogleMapsApiConfig, GoogleMapsMapIds} from '@models/google-maps-api-config';

declare let google;

@Injectable({
  providedIn: 'root',
})
export class GoogleMapsLibraryService {
  public readonly options: WritableSignal<GoogleMapsApiConfig | undefined> = signal(undefined);
  public readonly mapIds: WritableSignal<GoogleMapsMapIds | undefined> = signal(undefined);
  public readonly core: WritableSignal<google.maps.CoreLibrary | undefined> = signal(undefined);
  public readonly marker: WritableSignal<google.maps.MarkerLibrary | undefined> = signal(undefined);

  constructor(
    private appEnvironmentService: AppEnvironmentService,
    @Inject(PLATFORM_ID) private platformId: Object,
    private ngZone: NgZone,
  ) {
    // Add the Google Maps script to the page if it hasn't been added yet.
    if (isPlatformBrowser(this.platformId)) {
      afterNextRender(async () => {
        await this.ngZone.runOutsideAngular(async () => {
          // Check if the Google Maps API key is set in the environment.
          if (!this.appEnvironmentService.googleMapsApiKey) {
            console.warn('Google Maps API key is not set. Google Maps will not be loaded.');
            return;
          }

          console.log(
            'GoogleMapsLibraryService > constructor > appEnvironmentService.googleMapsApiKey:',
            this.appEnvironmentService.googleMapsApiKey,
          );

          // Fetch the content of the Google Maps script from the public assets directory.
          const response = await fetch('public/js/gmaps.js');
          const script = document.createElement('script');

          // Replace the placeholder in the script with the actual API key.
          const scriptContent = await response.text();
          script.textContent = scriptContent.replace(
            '__GOOGLE_MAPS_API_KEY__',
            this.appEnvironmentService.googleMapsApiKey,
          );

          document.head.appendChild(script);

          console.log(
            'Added Google Maps script to the page:',
            '\n===========================================\n',
            script.textContent,
            '\n===========================================\n',
          );

          // Trigger the loading of the Google Maps library.
          await this.load();
        });
      });
    }

    effect(async () => {
      if (this.options()) {
        await this.load();
      }
    });

    effect(async () => {
      if (this.appEnvironmentService.props()) {
        this.mapIds.set(this.appEnvironmentService.googleMapsMapIds);
      }
    });
  }

  set googleMapsApiConfig(value: GoogleMapsApiConfig) {
    this.options.set(value);
  }

  get googleMapsApiConfig(): GoogleMapsApiConfig {
    return this.options();
  }

  async load() {
    if (isPlatformServer(this.platformId)) return;

    await this.ngZone.runOutsideAngular(async () => {
      console.log('Loading Google Maps libraries...');

      const core = await google.maps.importLibrary('core');
      this.core.set(core as google.maps.CoreLibrary);
      console.log('google.maps.CoreLibrary loaded');

      const marker = await google.maps.importLibrary('marker');
      this.marker.set(marker as google.maps.MarkerLibrary);
      console.log('google.maps.MarkerLibrary loaded');
    });
  }
}
