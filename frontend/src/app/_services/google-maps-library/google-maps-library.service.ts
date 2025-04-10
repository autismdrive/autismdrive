/// <reference types="@types/google.maps" />
import {effect, Injectable, signal, WritableSignal} from '@angular/core';
import {GoogleMapsAPIWrapper} from '@ng-maps/google';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';

declare let google;

@Injectable({
  providedIn: 'root',
})
export class GoogleMapsLibraryService {
  public readonly core: WritableSignal<google.maps.CoreLibrary> = signal(undefined);

  constructor(
    private appEnvironmentService: AppEnvironmentService,
    private googleMapsAPIWrapper: GoogleMapsAPIWrapper,
  ) {
    console.log('GoogleMapsLibraryService > constructor');

    effect(() => {
      console.log(
        'GoogleMapsLibraryService > constructor > appEnvironmentService.googleMapsApiKey:',
        this.appEnvironmentService.googleMapsApiKey,
      );

      if (!appEnvironmentService.props()) return;

      this.googleMapsAPIWrapper['_loader'].configure({
        apiKey: appEnvironmentService.googleMapsApiKey,
        libraries: ['core', 'maps', 'geocoding']
      });

      google?.maps?.importLibrary('core').then(result => {
        console.log('GoogleMapsLibraryService > constructor > CoreLibrary imported.');
        this.core.set(result as google.maps.CoreLibrary);
      });
    });
  }
}
