/// <reference types="@types/google.maps" />

export enum GoogleMapsLibrary {
  CoreLibrary = 'core',
  MapsLibrary = 'maps',
  Maps3DLibrary = 'maps3d',
  PlacesLibrary = 'places',
  GeocodingLibrary = 'geocoding',
  RoutesLibrary = 'routes',
  MarkerLibrary = 'marker',
  GeometryLibrary = 'geometry',
  ElevationLibrary = 'elevation',
  StreetViewLibrary = 'streetView',
  JourneySharingLibrary = 'journeySharing',
  DrawingLibrary = 'drawing',
  VisualizationLibrary = 'visualization',
  AirQualityLibrary = 'airQuality',
  AddressValidationLibrary = 'addressValidation',
}

export interface GoogleMapsApiConfig {
  apiKey: string;
  libraries: GoogleMapsLibrary[];
}

export interface GoogleMapsMapIds {
  resourceDetailsPage: string;
  searchPage: string;
}
