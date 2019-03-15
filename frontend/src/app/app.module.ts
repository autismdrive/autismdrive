import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { Injectable, NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule } from '@angular/forms';
import {
  MAT_LABEL_GLOBAL_OPTIONS,
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
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatSelectModule,
  MatSidenavModule,
  MatSlideToggleModule,
  MatStepperModule,
  MatTableModule,
  MatToolbarModule,
  MAT_FORM_FIELD_DEFAULT_OPTIONS
} from '@angular/material';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CovalentTextEditorModule } from '@covalent/text-editor';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import { FormlyMatDatepickerModule } from '@ngx-formly/material/datepicker';
import { ColorPickerModule } from 'ngx-color-picker';
import { FileDropModule } from 'ngx-file-drop';
import { MarkdownModule } from 'ngx-markdown';
import { NgProgressModule } from 'ngx-progressbar';
import { ApiService } from './_services/api/api.service';
import { AppComponent } from './app.component';
import { EnrollComponent } from './enroll/enroll.component';
import { FiltersComponent } from './filters/filters.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { CardWrapperComponent } from './_forms/card-wrapper/card-wrapper.component';
import { HelpWrapperComponent } from './_forms/help-wrapper/help-wrapper.component';
import { RepeatSectionComponent } from './_forms/repeat-section/repeat-section.component';
import { EmailValidator, EmailValidatorMessage, PhoneValidator, PhoneValidatorMessage } from './_forms/validators/formly.validator';
import { HomeComponent } from './home/home.component';
import { LoadingComponent } from './loading/loading.component';
import { LoginComponent } from './login/login.component';
import { LogoComponent } from './logo/logo.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';
import { ProfileComponent } from './profile/profile.component';
import { QuestionnaireStepComponent } from './questionnaire-step/questionnaire-step.component';
import { QuestionnaireStepsListComponent } from './questionnaire-steps-list/questionnaire-steps-list.component';
import { RegisterComponent } from './register/register.component';
import { ResourceDetailComponent } from './resource-detail/resource-detail.component';
import { ResourcesComponent } from './resources/resources.component';
import { RoutingModule } from './_routing/routing.module';
import { SearchResultComponent } from './search-result/search-result.component';
import { StudiesComponent } from './studies/studies.component';
import { StudyDetailComponent } from './study-detail/study-detail.component';
import { TermsComponent } from './terms/terms.component';
import { TrainingDetailComponent } from './training-detail/training-detail.component';
import { FlowComponent } from './flow/flow.component';
import { ParticipantProfileComponent } from './participant-profile/participant-profile.component';
import { IntervalService } from './_services/interval/interval.service';
import { TimedoutComponent } from './timed-out/timed-out.component';
import { LogoutComponent } from './logout/logout.component';
import { AvatarDialogComponent } from './avatar-dialog/avatar-dialog.component';
import { FlowCompleteComponent } from './flow-complete/flow-complete.component';
import { FlowIntroComponent } from './flow-intro/flow-intro.component';
import {OverlayContainer} from '@angular/cdk/overlay';
import {JwtInterceptor} from './_routing/jwt-interceptor';
import {ErrorInterceptor} from './_routing/error-interceptor';

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
    AppComponent,
    CardWrapperComponent,
    EnrollComponent,
    FiltersComponent,
    ForgotPasswordComponent,
    HomeComponent,
    LoginComponent,
    LogoComponent,
    PasswordResetComponent,
    ProfileComponent,
    RegisterComponent,
    ResourcesComponent,
    SearchResultComponent,
    StudiesComponent,
    TermsComponent,
    FiltersComponent,
    SearchResultComponent,
    ResourceDetailComponent,
    StudyDetailComponent,
    TrainingDetailComponent,
    LoadingComponent,
    HelpWrapperComponent,
    QuestionnaireStepsListComponent,
    QuestionnaireStepComponent,
    RepeatSectionComponent,
    FlowComponent,
    ParticipantProfileComponent,
    TimedoutComponent,
    LogoutComponent,
    AvatarDialogComponent,
    FlowCompleteComponent,
    FlowIntroComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    ColorPickerModule,
    CommonModule,
    CovalentTextEditorModule,
    FileDropModule,
    FlexLayoutModule,
    FormlyMaterialModule,
    FormlyModule.forRoot(FormlyConfig.config),
    HttpClientModule,
    MarkdownModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatNativeDateModule,
    MatSidenavModule,
    FormlyMatDatepickerModule,
    MatDatepickerModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatStepperModule,
    MatTableModule,
    MatToolbarModule,
    NgProgressModule,
    ReactiveFormsModule,
    RoutingModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    ApiService,
    IntervalService,
    { provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,  useValue: { appearance: 'outline' }}
  ],
  bootstrap: [AppComponent],
  entryComponents: [AvatarDialogComponent]
})
export class AppModule {
  constructor(overlayContainer: OverlayContainer) {
    overlayContainer.getContainerElement().classList.add('stardrive-theme');
  }
}
