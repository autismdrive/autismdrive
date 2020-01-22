import {AgmCoreModule, LAZY_MAPS_API_CONFIG} from '@agm/core';
import {AgmJsMarkerClustererModule} from '@agm/js-marker-clusterer';
import {OverlayContainer} from '@angular/cdk/overlay';
import {CommonModule} from '@angular/common';
import {HTTP_INTERCEPTORS, HttpClient, HttpClientModule} from '@angular/common/http';
import {APP_INITIALIZER, Injectable, NgModule} from '@angular/core';
import {FlexLayoutModule} from '@angular/flex-layout';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MAT_FORM_FIELD_DEFAULT_OPTIONS, MatNativeDateModule, MatTabsModule} from '@angular/material';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatChipsModule} from '@angular/material/chips';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatDialogModule} from '@angular/material/dialog';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatListModule} from '@angular/material/list';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatRadioModule} from '@angular/material/radio';
import {MatSelectModule} from '@angular/material/select';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatSortModule} from '@angular/material/sort';
import {MatStepperModule} from '@angular/material/stepper';
import {MatTableModule} from '@angular/material/table';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatTreeModule} from '@angular/material/tree';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {DeviceDetectorModule} from 'ngx-device-detector';
import {MarkdownModule} from 'ngx-markdown';
import {NgProgressModule} from 'ngx-progressbar';
import {Observable, ObservableInput, of} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {environment} from '../environments/environment';
import {AutocompleteSectionComponent} from './_forms/autocomplete-section/autocomplete-section.component';
import {CardWrapperComponent} from './_forms/card-wrapper/card-wrapper.component';
import {FormPrintoutComponent} from './_forms/form-printout/form-printout.component';
import {HelpWrapperComponent} from './_forms/help-wrapper/help-wrapper.component';
import {MultiselectTreeComponent} from './_forms/multiselect-tree/multiselect-tree.component';
import {RepeatSectionDialogComponent} from './_forms/repeat-section-dialog/repeat-section-dialog.component';
import {RepeatSectionComponent} from './_forms/repeat-section/repeat-section.component';
import {
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
  UrlValidatorMessage
} from './_forms/validators/formly.validator';
import {ErrorInterceptor} from './_routing/error-interceptor';
import {JwtInterceptor} from './_routing/jwt-interceptor';
import {RoutingModule} from './_routing/routing.module';
import {ApiService} from './_services/api/api.service';
import {SearchService} from './_services/api/search.service';
import {ConfigService} from './_services/config.service';
import {IntervalService} from './_services/interval/interval.service';
import {AboutComponent} from './about/about.component';
import {AccordionComponent} from './accordion/accordion.component';
import {AddButtonComponent} from './add-button/add-button.component';
import {AdminExportDetailsComponent} from './admin-export-details/admin-export-details.component';
import {AdminExportComponent} from './admin-export/admin-export.component';
import {AdminHomeComponent} from './admin-home/admin-home.component';
import {AdminNoteDisplayComponent} from './admin-note-display/admin-note-display.component';
import {AdminNoteFormComponent} from './admin-note-form/admin-note-form.component';
import {AppComponent} from './app.component';
import {AvatarDialogComponent} from './avatar-dialog/avatar-dialog.component';
import {BorderBoxTileComponent} from './border-box-tile/border-box-tile.component';
import {ContactItemComponent} from './contact-item/contact-item.component';
import {DetailsLinkComponent} from './details-link/details-link.component';
import {EditButtonComponent} from './edit-button/edit-button.component';
import {EventDateComponent} from './event-date/event-date.component';
import {FilterChipsComponent} from './filter-chips/filter-chips.component';
import {FiltersComponent} from './filters/filters.component';
import {FlowCompleteComponent} from './flow-complete/flow-complete.component';
import {FlowIntroComponent} from './flow-intro/flow-intro.component';
import {FlowComponent} from './flow/flow.component';
import {FooterComponent} from './footer/footer.component';
import {ForgotPasswordComponent} from './forgot-password/forgot-password.component';
import {GoogleAnalyticsService} from './google-analytics.service';
import {HeaderComponent} from './header/header.component';
import {HeroSlidesComponent} from './hero-slides/hero-slides.component';
import {HomeComponent} from './home/home.component';
import {LastUpdatedDateComponent} from './last-updated-date/last-updated-date.component';
import {LoadingComponent} from './loading/loading.component';
import {LoginComponent} from './login/login.component';
import {LogoComponent} from './logo/logo.component';
import {LogoutComponent} from './logout/logout.component';
import {MirrorComponent} from './mirror/mirror.component';
import {NewsItemComponent} from './news-item/news-item.component';
import {ParticipantAdminComponent} from './participant-admin/participant-admin.component';
import {ParticipantDetailComponent} from './participant-detail/participant-detail.component';
import {ParticipantProfileComponent} from './participant-profile/participant-profile.component';
import {PasswordResetComponent} from './password-reset/password-reset.component';
import {ProfileComponent} from './profile/profile.component';
import {QuestionnaireDataTableComponent} from './questionnaire-data-table/questionnaire-data-table.component';
import {QuestionnaireDataViewComponent} from './questionnaire-data-view/questionnaire-data-view.component';
import {QuestionnaireStepComponent} from './questionnaire-step/questionnaire-step.component';
import {QuestionnaireStepsListComponent} from './questionnaire-steps-list/questionnaire-steps-list.component';
import {RegisterComponent} from './register/register.component';
import {RelatedItemsComponent} from './related-items/related-items.component';
import {ResourceDetailComponent} from './resource-detail/resource-detail.component';
import {ResourceFormComponent} from './resource-form/resource-form.component';
import {SearchBoxComponent} from './search-box/search-box.component';
import {SearchFilterComponent} from './search-filter/search-filter.component';
import {SearchResultComponent} from './search-result/search-result.component';
import {SearchTopicsComponent} from './search-topics/search-topics.component';
import {SearchComponent} from './search/search.component';
import {StudiesComponent} from './studies/studies.component';
import {StudyDetailComponent} from './study-detail/study-detail.component';
import {StudyFormComponent} from './study-form/study-form.component';
import {StudyInquiryComponent} from './study-inquiry/study-inquiry.component';
import {TermsComponent} from './terms/terms.component';
import {TimedoutComponent} from './timed-out/timed-out.component';
import {TypeIconComponent} from './type-icon/type-icon.component';
import {UserAdminDetailsComponent} from './user-admin-details/user-admin-details.component';
import {UserAdminComponent} from './user-admin/user-admin.component';
import {UvaEducationComponent} from './uva-education/uva-education.component';

// Attempt to load the configuration from a file called config.json right next to
// this index page, it if exists.  Otherwise assume we are connecting to port
// 5000 on the local server.
export function load(http: HttpClient, config: ConfigService): (() => Promise<boolean>) {
  return (): Promise<boolean> => {
    return new Promise<boolean>((resolve: (a: boolean) => void): void => {
      let url = './api/config';
      if ('override_config_url' in environment) {
        url = environment['override_config_url'];
      }
      http.get(url)
        .pipe(
          map((fromServer) => {
            config.fromProperties(fromServer);
            resolve(true);
          }),
          catchError((x: { status: number }, caught: Observable<void>): ObservableInput<{}> => {
            console.log('Failed to load configuration, unable to find ./api/config');
            resolve(false);
            return of({});
          })
        ).subscribe();
    });
  };
}

@Injectable()
export class FormlyConfig {
  public static config = {
    extras: {
      showError: ShowError,
    },
    types: [
      {name: 'repeat', component: RepeatSectionComponent},
      {
        name: 'multiselecttree',
        component: MultiselectTreeComponent,
        wrappers: ['card'],
      },
      {
        name: 'autocomplete',
        component: AutocompleteSectionComponent,
        wrappers: ['form-field'],
      }
    ],
    validators: [
      {name: 'phone', validation: PhoneValidator},
      {name: 'email', validation: EmailValidator},
      {name: 'url', validation: UrlValidator},
      {name: 'multicheckbox', validation: MulticheckboxValidator},
    ],
    validationMessages: [
      {name: 'phone', message: PhoneValidatorMessage},
      {name: 'email', message: EmailValidatorMessage},
      {name: 'url', message: UrlValidatorMessage},
      {name: 'multicheckbox', message: MulticheckboxValidatorMessage},
      {name: 'required', message: 'This field is required.'},
      {name: 'min', message: MinValidationMessage},
      {name: 'max', message: MaxValidationMessage},
    ],
    wrappers: [
      {name: 'help', component: HelpWrapperComponent},
      {name: 'card', component: CardWrapperComponent},
    ]
  };
}

@NgModule({
  declarations: [
    AboutComponent,
    AccordionComponent,
    AdminExportComponent,
    AdminExportDetailsComponent,
    AdminHomeComponent,
    AppComponent,
    AutocompleteSectionComponent,
    AvatarDialogComponent,
    AvatarDialogComponent,
    BorderBoxTileComponent,
    CardWrapperComponent,
    FilterChipsComponent,
    DetailsLinkComponent,
    FiltersComponent,
    FiltersComponent,
    FlowCompleteComponent,
    FlowCompleteComponent,
    FlowComponent,
    FlowIntroComponent,
    FlowIntroComponent,
    FooterComponent,
    ForgotPasswordComponent,
    FormPrintoutComponent,
    HeaderComponent,
    HelpWrapperComponent,
    HeroSlidesComponent,
    HomeComponent,
    LoadingComponent,
    LoginComponent,
    LogoComponent,
    LogoutComponent,
    LogoutComponent,
    MirrorComponent,
    NewsItemComponent,
    ParticipantDetailComponent,
    ParticipantProfileComponent,
    PasswordResetComponent,
    ProfileComponent,
    QuestionnaireDataTableComponent,
    QuestionnaireDataViewComponent,
    QuestionnaireStepComponent,
    QuestionnaireStepsListComponent,
    RegisterComponent,
    RepeatSectionComponent,
    RepeatSectionDialogComponent,
    ResourceDetailComponent,
    ResourceFormComponent,
    SearchBoxComponent,
    SearchComponent,
    SearchResultComponent,
    SearchResultComponent,
    StudiesComponent,
    StudyDetailComponent,
    StudyFormComponent,
    StudyInquiryComponent,
    TermsComponent,
    TimedoutComponent,
    TypeIconComponent,
    UserAdminComponent,
    UserAdminDetailsComponent,
    SearchTopicsComponent,
    SearchFilterComponent,
    AdminNoteFormComponent,
    AdminNoteDisplayComponent,
    EventDateComponent,
    LastUpdatedDateComponent,
    RelatedItemsComponent,
    ContactItemComponent,
    AddButtonComponent,
    EditButtonComponent,
    ParticipantAdminComponent,
    UvaEducationComponent,
    MultiselectTreeComponent,
  ],
  imports: [
    AgmCoreModule.forRoot(), // Config provided by ConfService (see providers below)
    AgmJsMarkerClustererModule,
    BrowserAnimationsModule,
    BrowserModule,
    CommonModule,
    DeviceDetectorModule.forRoot(),
    FlexLayoutModule,
    FormlyMatDatepickerModule,
    FormlyMaterialModule,
    FormlyModule.forRoot(FormlyConfig.config),
    FormsModule,
    HttpClientModule,
    MarkdownModule.forRoot(),
    MatAutocompleteModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDatepickerModule,
    MatDialogModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatSelectModule,
    MatSidenavModule,
    MatSlideToggleModule,
    MatSortModule,
    MatStepperModule,
    MatTabsModule,
    MatTableModule,
    MatToolbarModule,
    MatTooltipModule,
    NgProgressModule,
    PdfJsViewerModule,
    ReactiveFormsModule,
    RoutingModule,
    MatTreeModule,
    MatBadgeModule,
  ],
  providers: [
    {provide: APP_INITIALIZER, useFactory: load, deps: [HttpClient, ConfigService], multi: true},
    {provide: LAZY_MAPS_API_CONFIG, useExisting: ConfigService},
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true},
    {provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: {appearance: 'outline'}},
    ApiService,
    GoogleAnalyticsService,
    IntervalService,
    SearchService,
  ],
  bootstrap: [AppComponent],
  entryComponents: [
    AdminExportDetailsComponent,
    AvatarDialogComponent,
    RepeatSectionDialogComponent,
    AdminNoteFormComponent
  ]
})
export class AppModule {
  constructor(overlayContainer: OverlayContainer) {
    overlayContainer.getContainerElement().classList.add('stardrive-theme');
  }
}
