import {OverlayContainer} from '@angular/cdk/overlay';
import {CommonModule, DatePipe} from '@angular/common';
import {HTTP_INTERCEPTORS, HttpClient, HttpClientModule} from '@angular/common/http';
import {APP_INITIALIZER, Injectable, NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from '@angular/material/form-field';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {MaterialModule} from '@app/material/material.module';
import {environment} from '@environments/environment';
import {AutocompleteSectionComponent} from '@forms/autocomplete-section/autocomplete-section.component';
import {CardWrapperComponent} from '@forms/card-wrapper/card-wrapper.component';
import {FormPrintoutComponent} from '@forms/form-printout/form-printout.component';
import {GroupValidationWrapperComponent} from '@forms/group-validation-wrapper/group-validation-wrapper.component';
import {HelpWrapperComponent} from '@forms/help-wrapper/help-wrapper.component';
import {MultiselectTreeComponent} from '@forms/multiselect-tree/multiselect-tree.component';
import {RepeatSectionDialogComponent} from '@forms/repeat-section-dialog/repeat-section-dialog.component';
import {RepeatSectionComponent} from '@forms/repeat-section/repeat-section.component';
import {ResizeTextareaComponent} from '@forms/resize-textarea/resize-textarea.component';
import {TreeComponent} from '@forms/tree/tree.component';
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
import {NgMapsCoreModule} from '@ng-maps/core';
import {GOOGLE_MAPS_API_CONFIG, NgMapsGoogleModule} from '@ng-maps/google';
import {NgMapsMarkerClustererModule} from '@ng-maps/marker-clusterer';
import {FormlyModule} from '@ngx-formly/core';
import {FormlyMaterialModule} from '@ngx-formly/material';
import {FormlyMatDatepickerModule} from '@ngx-formly/material/datepicker';
import {FlexLayoutModule} from '@node_modules/@ngbracket/ngx-layout';
import {ErrorInterceptor} from '@routing/error-interceptor';
import {JwtInterceptor} from '@routing/jwt-interceptor';
import {RoutingModule} from '@routing/routing.module';
import {ApiService} from '@services/api/api.service';
import {CategoriesService} from '@services/categories/categories.service';
import {ConfigService} from '@services/config/config.service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';
import {IntervalService} from '@services/interval/interval.service';
import {SearchService} from '@services/search/search.service';
import {TruncateModule} from '@yellowspot/ng-truncate';
import {PdfJsViewerModule} from 'ng2-pdfjs-viewer';
import {DeviceDetectorService} from 'ngx-device-detector';
import {MarkdownModule} from 'ngx-markdown';
import {NgProgressModule} from 'ngx-progressbar';
import {lastValueFrom, of} from 'rxjs';
import {catchError} from 'rxjs/operators';
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
import {Covid19ResourcesComponent} from './covid19-resources/covid19-resources.component';
import {DetailsLinkComponent} from './details-link/details-link.component';
import {EditButtonComponent} from './edit-button/edit-button.component';
import {EmailLogAdminComponent} from './email-log-admin/email-log-admin.component';
import {EventDateComponent} from './event-date/event-date.component';
import {EventRegistrationFormComponent} from './event-registration-form/event-registration-form.component';
import {EventRegistrationComponent} from './event-registration/event-registration.component';
import {FavoriteResourceButtonComponent} from './favorite-resource-button/favorite-resource-button.component';
import {FavoriteResourcesComponent} from './favorite-resources/favorite-resources.component';
import {FavoriteTopicsDialogComponent} from './favorite-topics-dialog/favorite-topics-dialog.component';
import {FavoriteTopicsComponent} from './favorite-topics/favorite-topics.component';
import {FilterChipsComponent} from './filter-chips/filter-chips.component';
import {FiltersComponent} from './filters/filters.component';
import {FlowCompleteComponent} from './flow-complete/flow-complete.component';
import {FlowIntroComponent} from './flow-intro/flow-intro.component';
import {FlowComponent} from './flow/flow.component';
import {FooterComponent} from './footer/footer.component';
import {ForgotPasswordComponent} from './forgot-password/forgot-password.component';
import {HeaderComponent} from './header/header.component';
import {HeroSlidesComponent} from './hero-slides/hero-slides.component';
import {HomeComponent} from './home/home.component';
import {InvestigatorFormComponent} from './investigator-form/investigator-form.component';
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
import {ProfileMetaComponent} from './profile_meta/profile_meta.component';
import {QuestionnaireDataTableComponent} from './questionnaire-data-table/questionnaire-data-table.component';
import {QuestionnaireDataViewComponent} from './questionnaire-data-view/questionnaire-data-view.component';
import {QuestionnaireStepComponent} from './questionnaire-step/questionnaire-step.component';
import {QuestionnaireStepsListComponent} from './questionnaire-steps-list/questionnaire-steps-list.component';
import {RegisterDialogComponent} from './register-dialog/register-dialog.component';
import {RegisterComponent} from './register/register.component';
import {RelatedItemsComponent} from './related-items/related-items.component';
import {ResourceDetailComponent} from './resource-detail/resource-detail.component';
import {ResourceFormComponent} from './resource-form/resource-form.component';
import {SearchBoxComponent} from './search-box/search-box.component';
import {SearchFilterComponent} from './search-filter/search-filter.component';
import {SearchFiltersBreadcrumbsComponent} from './search-filters-breadcrumbs/search-filters-breadcrumbs.component';
import {SearchResultComponent} from './search-result/search-result.component';
import {SearchSortComponent} from './search-sort/search-sort.component';
import {SearchTopicsComponent} from './search-topics/search-topics.component';
import {SearchComponent} from './search/search.component';
import {SkillstarAdminComponent} from './skillstar-admin/skillstar-admin.component';
import {StudiesComponent} from './studies/studies.component';
import {StudyDetailComponent} from './study-detail/study-detail.component';
import {StudyFormComponent} from './study-form/study-form.component';
import {StudyInquiryComponent} from './study-inquiry/study-inquiry.component';
import {StudySurveyEntryComponent} from './study-survey-entry/study-survey-entry.component';
import {TaxonomyAdminComponent} from './taxonomy-admin/taxonomy-admin.component';
import {TermsComponent} from './terms/terms.component';
import {TimedoutComponent} from './timed-out/timed-out.component';
import {TutorialVideoComponent} from './tutorial-video/tutorial-video.component';
import {TypeIconComponent} from './type-icon/type-icon.component';
import {UserAdminDetailsComponent} from './user-admin-details/user-admin-details.component';
import {UserAdminComponent} from './user-admin/user-admin.component';
import {UvaEducationComponent} from './uva-education/uva-education.component';

// Attempt to load the configuration from a file called config.json right next to
// this index page, it if exists. Otherwise, assume we are connecting to port
// 5000 on the local server.
export const load = (http: HttpClient, config: ConfigService): (() => Promise<boolean>) => {
  return async (): Promise<boolean> => {
    let url = './api/config';
    if ('override_config_url' in environment) {
      url = environment['override_config_url'];
    }

    try {
      const configFromJsonFile = await lastValueFrom(
        http.get(url, {responseType: 'json'}).pipe(
          catchError(() => {
            return of(false);
          }),
        ),
      );
      if (configFromJsonFile) {
        config.fromProperties(configFromJsonFile);
      }
      return !!configFromJsonFile;
    } catch (e) {
      return false;
    }
  };
};

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
      },
      {
        name: 'textarea-auto-resize',
        component: ResizeTextareaComponent,
        wrappers: ['form-field'],
      },
    ],
    validators: [
      {name: 'phone', validation: PhoneValidator},
      {name: 'email', validation: EmailValidator},
      {name: 'url', validation: UrlValidator},
      {name: 'multicheckbox', validation: MulticheckboxValidator},
      {name: 'emailConfirm', validation: EmailMatchValidator},
    ],
    validationMessages: [
      {name: 'phone', message: PhoneValidatorMessage},
      {name: 'email', message: EmailValidatorMessage},
      {name: 'emailConfirm', message: EmailMatchValidatorMessage},
      {name: 'url', message: UrlValidatorMessage},
      {name: 'multicheckbox', message: MulticheckboxValidatorMessage},
      {name: 'required', message: 'This field is required.'},
      {name: 'min', message: MinValidationMessage},
      {name: 'max', message: MaxValidationMessage},
    ],
    wrappers: [
      {name: 'help', component: HelpWrapperComponent},
      {name: 'card', component: CardWrapperComponent},
      {name: 'group-validation', component: GroupValidationWrapperComponent},
    ],
  };
}

@NgModule({
  declarations: [
    AboutComponent,
    AccordionComponent,
    AddButtonComponent,
    AdminExportComponent,
    AdminExportDetailsComponent,
    AdminHomeComponent,
    AdminNoteDisplayComponent,
    AdminNoteFormComponent,
    AppComponent,
    AutocompleteSectionComponent,
    AvatarDialogComponent,
    AvatarDialogComponent,
    BorderBoxTileComponent,
    CardWrapperComponent,
    ContactItemComponent,
    Covid19ResourcesComponent,
    DetailsLinkComponent,
    EditButtonComponent,
    EmailLogAdminComponent,
    EventDateComponent,
    EventRegistrationComponent,
    EventRegistrationFormComponent,
    FavoriteResourceButtonComponent,
    FavoriteResourcesComponent,
    FavoriteTopicsComponent,
    FavoriteTopicsDialogComponent,
    FilterChipsComponent,
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
    InvestigatorFormComponent,
    LastUpdatedDateComponent,
    LoadingComponent,
    LoginComponent,
    LogoComponent,
    LogoutComponent,
    LogoutComponent,
    MirrorComponent,
    MultiselectTreeComponent,
    NewsItemComponent,
    ParticipantAdminComponent,
    ParticipantDetailComponent,
    ParticipantProfileComponent,
    PasswordResetComponent,
    ProfileComponent,
    QuestionnaireDataTableComponent,
    QuestionnaireDataViewComponent,
    QuestionnaireStepComponent,
    QuestionnaireStepsListComponent,
    RegisterComponent,
    RegisterDialogComponent,
    RelatedItemsComponent,
    RepeatSectionComponent,
    RepeatSectionDialogComponent,
    ResourceDetailComponent,
    ResourceFormComponent,
    SearchBoxComponent,
    SearchComponent,
    SearchFilterComponent,
    SearchFiltersBreadcrumbsComponent,
    SearchResultComponent,
    SearchResultComponent,
    SearchSortComponent,
    SearchTopicsComponent,
    StudiesComponent,
    StudyDetailComponent,
    StudyFormComponent,
    StudyInquiryComponent,
    StudySurveyEntryComponent,
    TaxonomyAdminComponent,
    TermsComponent,
    TimedoutComponent,
    TreeComponent,
    TutorialVideoComponent,
    TypeIconComponent,
    UserAdminComponent,
    UserAdminDetailsComponent,
    UvaEducationComponent,
    SkillstarAdminComponent,
    ResizeTextareaComponent,
    ProfileMetaComponent,
    GroupValidationWrapperComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    CommonModule,
    FlexLayoutModule,
    FormlyMatDatepickerModule,
    FormlyMaterialModule,
    FormlyModule,
    FormsModule,
    HttpClientModule,
    MarkdownModule.forRoot(),
    MaterialModule,
    NgMapsCoreModule,
    NgMapsGoogleModule,
    NgMapsMarkerClustererModule,
    NgProgressModule,
    PdfJsViewerModule,
    ReactiveFormsModule,
    TruncateModule,
    YouTubePlayerModule,
    RoutingModule, // This line must be the last module imported
  ],
  providers: [
    ApiService,
    CategoriesService,
    DatePipe,
    DeviceDetectorService,
    GoogleAnalyticsService,
    IntervalService,
    SearchService,
    {provide: APP_INITIALIZER, useFactory: load, deps: [HttpClient, ConfigService], multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true},
    {provide: GOOGLE_MAPS_API_CONFIG, useValue: {apiKey: environment.google_maps_api_key}},
    {provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: {appearance: 'outline'}},
  ],
  bootstrap: [AppComponent],
})
export class AppModule {
  constructor(overlayContainer: OverlayContainer) {
    overlayContainer.getContainerElement().classList.add('stardrive-theme');
  }
}
