import {CommonModule, DatePipe} from '@angular/common';
import {provideHttpClient, withInterceptors} from '@angular/common/http';
import {enableProdMode, importProvidersFrom, inject, provideAppInitializer} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from '@angular/material/form-field';
import {bootstrapApplication, BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule, provideAnimations} from '@angular/platform-browser/animations';
import {provideRouter, withHashLocation, withInMemoryScrolling, withRouterConfig} from '@angular/router';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {AppComponent} from '@app/app.component';
import {FormlyConfig} from '@app/app.config';
import {environment} from '@environments/environment';
import {NgMapsCoreModule} from '@ng-maps/core';
import {GOOGLE_MAPS_API_CONFIG, GoogleMapsAPIWrapper, NgMapsGoogleModule} from '@ng-maps/google';
import {NgMapsMarkerClustererModule} from '@ng-maps/marker-clusterer';
import {FlexLayoutModule} from '@ngbracket/ngx-layout';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {errorInterceptor} from '@routing/error-interceptor';
import {jwtInterceptor} from '@routing/jwt-interceptor';
import {routes} from '@routing/routes';
import {ApiService} from '@services/api/api.service';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {CategoriesService} from '@services/categories/categories.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {googleMapsApiConfigFactory} from '@services/google-maps-library/google-maps-api-config';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {IntervalService} from '@services/interval/interval.service';
import {SearchService} from '@services/search/search.service';
import {TruncateModule} from '@yellowspot/ng-truncate';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {DeviceDetectorService} from 'ngx-device-detector';
import {MarkdownModule} from 'ngx-markdown';
import {appInitializer} from './app-initializer';

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
  providers: [
    provideAppInitializer(appInitializer),
    provideHttpClient(withInterceptors([jwtInterceptor, errorInterceptor])),
    {
      provide: GOOGLE_MAPS_API_CONFIG,
      useFactory: googleMapsApiConfigFactory,
      useValue: {
        apiKey: environment.googleMapsApiKey,
        libraries: ['maps', 'marker', 'geocoding'],
      },
    },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {appearance: 'outline'},
    },
    provideRouter(
      routes,
      withHashLocation(),
      withRouterConfig({urlUpdateStrategy: 'eager'}),
      withInMemoryScrolling({scrollPositionRestoration: 'enabled'}),
    ),
    provideAnimations(),
    importProvidersFrom(
      BrowserAnimationsModule,
      BrowserModule,
      CommonModule,
      FlexLayoutModule,
      FormlyMatDatepickerModule,
      FormlyMaterialModule,
      FormlyModule.forRoot(FormlyConfig.config),
      FormsModule,
      MarkdownModule.forRoot(),
      NgMapsCoreModule,
      NgMapsGoogleModule,
      NgMapsMarkerClustererModule,
      PdfJsViewerModule,
      ReactiveFormsModule,
      TruncateModule,
      YouTubePlayerModule,
    ),
    ApiService,
    AuthenticationService,
    CategoriesService,
    AppEnvironmentService,
    DatePipe,
    DeviceDetectorService,
    GoogleAnalyticsService,
    GoogleMapsLibraryService,
    GoogleMapsAPIWrapper,
    IntervalService,
    SearchService,
  ],
}).catch(err => console.error(err));
