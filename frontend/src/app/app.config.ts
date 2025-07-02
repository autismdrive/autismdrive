import {CommonModule, DatePipe, isPlatformServer} from '@angular/common';
import {provideHttpClient, withFetch, withInterceptors, withInterceptorsFromDi} from '@angular/common/http';
import {
  importProvidersFrom,
  LOCALE_ID,
  PLATFORM_ID,
  provideAppInitializer,
  provideZoneChangeDetection,
} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {GoogleMapsModule} from '@angular/google-maps';
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from '@angular/material/form-field';
import {
  BrowserModule,
  provideClientHydration,
  withEventReplay,
  withHttpTransferCacheOptions,
} from '@angular/platform-browser';
import {BrowserAnimationsModule, provideAnimations} from '@angular/platform-browser/animations';
import {
  provideRouter,
  withComponentInputBinding,
  withHashLocation,
  withInMemoryScrolling,
  withRouterConfig,
} from '@angular/router';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {
  googleMapsApiConfigFactory,
  googleMapsMapIdsFactory,
} from '@app/shared/services/google-maps-library/google-maps-api-config';
import {CardWrapperComponent} from '@forms/card-wrapper/card-wrapper.component';
import {CategoriesSelectTreeComponent} from '@forms/categories-select-tree/categories-select-tree.component';
import {GroupValidationWrapperComponent} from '@forms/group-validation-wrapper/group-validation-wrapper.component';
import {HelpWrapperComponent} from '@forms/help-wrapper/help-wrapper.component';
import {RepeatSectionComponent} from '@forms/repeat-section/repeat-section.component';
import {
  EmailMatchValidator,
  EmailMatchValidatorMessage,
  EmailValidator,
  EmailValidatorMessage,
  MaxValidationMessage,
  MinValidationMessage,
  MulticheckboxValidator,
  MulticheckboxValidatorMessage,
  PhoneValidator,
  PhoneValidatorMessage,
  ShowError,
  UrlValidator,
  UrlValidatorMessage,
} from '@forms/validators/formly.validator';
import {FlexLayoutModule} from '@ngbracket/ngx-layout';
import {FormlyModule, provideFormlyCore} from '@ngx-formly/core';
import {FormlyMaterialModule, withFormlyMaterial} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {errorInterceptor} from '@routing/error-interceptor';
import {jwtInterceptor} from '@routing/jwt-interceptor';
import {clientRoutes} from '@routing/routes.client';
import {ApiService} from '@services/api/api.service';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {CategoriesService} from '@services/categories/categories.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {GoogleMapsLibraryService} from '@services/google-maps-library/google-maps-library.service';
import {IntervalService} from '@services/interval/interval.service';
import {SearchService} from '@services/search/search.service';
import {TruncateModule} from '@yellowspot/ng-truncate';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {DeviceDetectorService} from 'ngx-device-detector';
import {MarkdownModule} from 'ngx-markdown';
import {appInitializer} from '../app-initializer';
import {GOOGLE_MAPS_API_CONFIG, GOOGLE_MAPS_MAP_IDS, LOCAL_STORAGE} from './tokens';

export const customFormlyConfig = {
  extras: {
    showError: ShowError,
  },
  types: [
    {name: 'repeat', component: RepeatSectionComponent},
    {
      name: 'categorytree',
      component: CategoriesSelectTreeComponent,
      wrappers: ['card'],
    },
  ],
  validators: [
    {name: 'phone', validation: PhoneValidator},
    {name: 'email', validation: EmailValidator},
    {
      name: 'url',
      validation: UrlValidator,
    },
    {name: 'multicheckbox', validation: MulticheckboxValidator},
    {
      name: 'emailConfirm',
      validation: EmailMatchValidator,
    },
  ],
  validationMessages: [
    {name: 'phone', message: PhoneValidatorMessage},
    {
      name: 'email',
      message: EmailValidatorMessage,
    },
    {name: 'emailConfirm', message: EmailMatchValidatorMessage},
    {
      name: 'url',
      message: UrlValidatorMessage,
    },
    {name: 'multicheckbox', message: MulticheckboxValidatorMessage},
    {
      name: 'required',
      message: 'This field is required.',
    },
    {name: 'min', message: MinValidationMessage},
    {name: 'max', message: MaxValidationMessage},
  ],
  wrappers: [
    {name: 'help', component: HelpWrapperComponent},
    {
      name: 'card',
      component: CardWrapperComponent,
    },
    {name: 'group-validation', component: GroupValidationWrapperComponent},
  ],
};

export const appConfig = {
  providers: [
    {
      provide: LOCAL_STORAGE,
      useFactory: (platformId: object) => {
        if (isPlatformServer(platformId)) {
          return {}; // Return an empty object on the server
        }
        return localStorage; // Use the browser's localStorage
      },
      deps: [PLATFORM_ID],
    },
    provideZoneChangeDetection({eventCoalescing: true}),
    provideRouter(clientRoutes, withComponentInputBinding()),
    provideAnimations(),
    provideClientHydration(withEventReplay(), withHttpTransferCacheOptions({includePostRequests: true})),
    provideHttpClient(withInterceptorsFromDi(), withFetch()),
    importProvidersFrom(BrowserModule, CommonModule, FlexLayoutModule, ReactiveFormsModule),
    ApiService,
    provideFormlyCore([...withFormlyMaterial(), customFormlyConfig]),
    {provide: LOCALE_ID, useValue: 'en-US'},

    provideAppInitializer(appInitializer),
    provideHttpClient(withInterceptors([jwtInterceptor, errorInterceptor])),
    {
      provide: GOOGLE_MAPS_API_CONFIG,
      useFactory: googleMapsApiConfigFactory,
    },
    {
      provide: GOOGLE_MAPS_MAP_IDS,
      useFactory: googleMapsMapIdsFactory,
    },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {appearance: 'outline'},
    },
    provideRouter(
      clientRoutes,
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
      FormlyModule.forRoot(customFormlyConfig),
      FormsModule,
      GoogleMapsModule,
      MarkdownModule.forRoot(),
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
    IntervalService,
    SearchService,
  ],
};
