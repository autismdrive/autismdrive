import {effect, Injectable, signal, WritableSignal} from '@angular/core';
import {ConfigService} from '@services/config/config.service';

@Injectable({
  providedIn: 'root',
})
export class GoogleMapsLibraryService {
  public readonly core: WritableSignal<google.maps.CoreLibrary> = signal(undefined);
  public readonly maps: WritableSignal<google.maps.MapsLibrary> = signal(undefined);
  public readonly geocoding: WritableSignal<google.maps.GeocodingLibrary> = signal(undefined);

  constructor(private configService: ConfigService) {
    console.log('GoogleMapsLibraryService > constructor');

    effect(() => {
      console.log('GoogleMapsLibraryService > constructor > configService.apiKey:', this.configService.apiKey);

      if (!configService.props()) return;

      google.maps.importLibrary('core').then(result => {
        console.log('GoogleMapsLibraryService > constructor > CoreLibrary imported.')
        this.core.set(result as google.maps.CoreLibrary);
      });
      google.maps.importLibrary('maps').then(m => {
        console.log('GoogleMapsLibraryService > constructor > MapsLibrary imported.')
        this.maps.set(m as google.maps.MapsLibrary);
      });
      google.maps.importLibrary('geocoding').then(g => {
        console.log('GoogleMapsLibraryService > constructor > GeocodingLibrary imported.')
        this.geocoding.set(g as google.maps.GeocodingLibrary);
      });

    });
  }
}
