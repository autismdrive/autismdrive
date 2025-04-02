import {CommonModule, DatePipe} from '@angular/common';
import {provideHttpClient, withInterceptors} from '@angular/common/http';
import {enableProdMode, importProvidersFrom, provideAppInitializer} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from '@angular/material/form-field';
import {bootstrapApplication, BrowserModule} from '@angular/platform-browser';
import {provideAnimations} from '@angular/platform-browser/animations';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {AppComponent} from '@app/app.component';
import {FormlyConfig, load} from '@app/app.config';
import {environment} from '@environments/environment';
import {NgMapsCoreModule} from '@ng-maps/core';
import {GOOGLE_MAPS_API_CONFIG, NgMapsGoogleModule} from '@ng-maps/google';
import {NgMapsMarkerClustererModule} from '@ng-maps/marker-clusterer';
import {FlexLayoutModule} from '@ngbracket/ngx-layout';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {errorInterceptor} from '@routing/error-interceptor';
import {jwtInterceptor} from '@routing/jwt-interceptor';
import {RoutingModule} from '@routing/routing.module';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {CategoriesService} from '@services/categories/categories.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {IntervalService} from '@services/interval/interval.service';
import {SearchService} from '@services/search/search.service';
import {TruncateModule} from '@yellowspot/ng-truncate';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {DeviceDetectorService} from 'ngx-device-detector';
import {MarkdownModule} from 'ngx-markdown';

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(
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
      RoutingModule,
    ),
    ApiService,
    AuthenticationService,
    CategoriesService,
    DatePipe,
    DeviceDetectorService,
    GoogleAnalyticsService,
    IntervalService,
    SearchService,
    provideAppInitializer(() => {
      load();
    }),
    {
      provide: GOOGLE_MAPS_API_CONFIG,
      useValue: {apiKey: environment.google_maps_api_key},
    },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {appearance: 'outline'},
    },
    provideHttpClient(withInterceptors([errorInterceptor, jwtInterceptor])),
    provideAnimations(),
  ],
}).catch(err => console.error(err));
