import { AgmCoreModule } from '@agm/core';
import { AgmJsMarkerClustererModule } from '@agm/js-marker-clusterer';
import { OverlayContainer } from '@angular/cdk/overlay';
import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { Injectable, NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS, MatNativeDateModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSortModule } from '@angular/material/sort';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import { FormlyMatDatepickerModule } from '@ngx-formly/material/datepicker';
import { PdfJsViewerModule } from 'ng2-pdfjs-viewer';
import { ColorPickerModule } from 'ngx-color-picker';
import { MarkdownModule } from 'ngx-markdown';
import { NgProgressModule } from 'ngx-progressbar';
import { environment } from 'src/environments/environment';
import { CardWrapperComponent } from './_forms/card-wrapper/card-wrapper.component';
import { HelpWrapperComponent } from './_forms/help-wrapper/help-wrapper.component';
import { RepeatSectionComponent } from './_forms/repeat-section/repeat-section.component';
import { EmailValidator, EmailValidatorMessage, PhoneValidator, PhoneValidatorMessage } from './_forms/validators/formly.validator';
import { ErrorInterceptor } from './_routing/error-interceptor';
import { JwtInterceptor } from './_routing/jwt-interceptor';
import { RoutingModule } from './_routing/routing.module';
import { ApiService } from './_services/api/api.service';
import { SearchService } from './_services/api/search.service';
import { IntervalService } from './_services/interval/interval.service';
import { AccordionComponent } from './accordion/accordion.component';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { AppComponent } from './app.component';
import { AvatarDialogComponent } from './avatar-dialog/avatar-dialog.component';
import { CategoryChipsComponent } from './category-chips/category-chips.component';
import { EnrollComponent } from './enroll/enroll.component';
import { FiltersComponent } from './filters/filters.component';
import { FlowCompleteComponent } from './flow-complete/flow-complete.component';
import { FlowIntroComponent } from './flow-intro/flow-intro.component';
import { FlowComponent } from './flow/flow.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { HeaderComponent } from './header/header.component';
import { HeroSlidesComponent } from './hero-slides/hero-slides.component';
import { HomeComponent } from './home/home.component';
import { LoadingComponent } from './loading/loading.component';
import { LoginComponent } from './login/login.component';
import { LogoComponent } from './logo/logo.component';
import { LogoutComponent } from './logout/logout.component';
import { NewsItemComponent } from './news-item/news-item.component';
import { ParticipantDetailComponent } from './participant-detail/participant-detail.component';
import { ParticipantProfileComponent } from './participant-profile/participant-profile.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';
import { ProfileComponent } from './profile/profile.component';
import { QuestionnaireDataTableComponent } from './questionnaire-data-table/questionnaire-data-table.component';
import { QuestionnaireDataViewComponent } from './questionnaire-data-view/questionnaire-data-view.component';
import { QuestionnaireStepComponent } from './questionnaire-step/questionnaire-step.component';
import { QuestionnaireStepsListComponent } from './questionnaire-steps-list/questionnaire-steps-list.component';
import { RegisterComponent } from './register/register.component';
import { ResourceAddButtonComponent } from './resource-add-button/resource-add-button.component';
import { ResourceDetailComponent } from './resource-detail/resource-detail.component';
import { ResourceEditButtonComponent } from './resource-edit-button/resource-edit-button.component';
import { ResourceFormComponent } from './resource-form/resource-form.component';
import { ResourcesComponent } from './resources/resources.component';
import { SearchBoxComponent } from './search-box/search-box.component';
import { SearchResultComponent } from './search-result/search-result.component';
import { SearchComponent } from './search/search.component';
import { StudiesComponent } from './studies/studies.component';
import { StudyDetailComponent } from './study-detail/study-detail.component';
import { TermsComponent } from './terms/terms.component';
import { TimedoutComponent } from './timed-out/timed-out.component';
import { TypeIconComponent } from './type-icon/type-icon.component';
import { UserAdminDetailsComponent } from './user-admin-details/user-admin-details.component';
import { UserAdminComponent } from './user-admin/user-admin.component';

@Injectable()
export class FormlyConfig {
  public static config = {
    types: [
      { name: 'repeat', component: RepeatSectionComponent },
    ],
    validators: [
      { name: 'phone', validation: PhoneValidator },
      { name: 'email', validation: EmailValidator },
    ],
    validationMessages: [
      { name: 'phone', message: PhoneValidatorMessage },
      { name: 'email', message: EmailValidatorMessage },
      { name: 'required', message: 'This field is required.' },
    ],
    wrappers: [
      { name: 'help', component: HelpWrapperComponent },
      { name: 'card', component: CardWrapperComponent },
    ],
  };
}

@NgModule({
  declarations: [
    AccordionComponent,
    AdminHomeComponent,
    AppComponent,
    AvatarDialogComponent,
    AvatarDialogComponent,
    CardWrapperComponent,
    CategoryChipsComponent,
    EnrollComponent,
    FiltersComponent,
    FiltersComponent,
    FlowCompleteComponent,
    FlowCompleteComponent,
    FlowComponent,
    FlowIntroComponent,
    FlowIntroComponent,
    ForgotPasswordComponent,
    HeaderComponent,
    HelpWrapperComponent,
    HeroSlidesComponent,
    HomeComponent,
    LoadingComponent,
    LoginComponent,
    LogoComponent,
    LogoutComponent,
    LogoutComponent,
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
    ResourceAddButtonComponent,
    ResourceDetailComponent,
    ResourceEditButtonComponent,
    ResourceFormComponent,
    ResourcesComponent,
    SearchBoxComponent,
    SearchComponent,
    SearchResultComponent,
    SearchResultComponent,
    StudiesComponent,
    StudyDetailComponent,
    TermsComponent,
    TimedoutComponent,
    TypeIconComponent,
    UserAdminComponent,
    UserAdminDetailsComponent,
  ],
  imports: [
    AgmCoreModule.forRoot({ apiKey: environment.gc_api_key }),
    AgmJsMarkerClustererModule,
    BrowserAnimationsModule,
    BrowserModule,
    ColorPickerModule,
    CommonModule,
    FlexLayoutModule,
    FormlyMatDatepickerModule,
    FormlyMaterialModule,
    FormlyModule.forRoot(FormlyConfig.config),
    FormsModule,
    HttpClientModule,
    MarkdownModule.forRoot(),
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDatepickerModule,
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
    MatSelectModule,
    MatSidenavModule,
    MatSlideToggleModule,
    MatSortModule,
    MatStepperModule,
    MatTableModule,
    MatToolbarModule,
    MatTooltipModule,
    NgProgressModule,
    PdfJsViewerModule,
    ReactiveFormsModule,
    RoutingModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: { appearance: 'outline' } },
    ApiService,
    IntervalService,
    SearchService,
  ],
  bootstrap: [AppComponent],
  entryComponents: [AvatarDialogComponent]
})
export class AppModule {
  constructor(overlayContainer: OverlayContainer) {
    overlayContainer.getContainerElement().classList.add('stardrive-theme');
  }
}
