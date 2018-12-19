import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule } from '@angular/forms';
import {
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatFormFieldModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatSelectModule,
  MatToolbarModule,
  MatSlideToggleModule,
  MatTableModule
} from '@angular/material';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CovalentTextEditorModule } from '@covalent/text-editor';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import { ColorPickerModule } from 'ngx-color-picker';
import { MarkdownModule } from 'ngx-markdown';
import { ApiService } from './api.service';
import { AppComponent } from './app.component';
import { AuthInterceptor } from './AuthInterceptor';
import { EnrollComponent } from './enroll/enroll.component';
import { FiltersComponent } from './filters/filters.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { SDFileUploadComponent } from './forms/file-upload/file-upload.component';
import { SDFormFieldLabelComponent } from './forms/form-field-label/form-field-label.component';
import { SDFormFieldComponent } from './forms/form-field/form-field.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { LogoComponent } from './logo/logo.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';
import { ProfileComponent } from './profile/profile.component';
import { RegisterComponent } from './register/register.component';
import { ResourcesComponent } from './resources/resources.component';
import { RoutingModule } from './routing/routing.module';
import { SearchResultComponent } from './search-result/search-result.component';
import { StudiesComponent } from './studies/studies.component';
import { TermsComponent } from './terms/terms.component';
import { NgProgressModule } from 'ngx-progressbar';
import { FileDropModule } from 'ngx-file-drop';


@NgModule({
  declarations: [
    AppComponent,
    EnrollComponent,
    ForgotPasswordComponent,
    HomeComponent,
    LoginComponent,
    LogoComponent,
    PasswordResetComponent,
    ProfileComponent,
    RegisterComponent,
    ResourcesComponent,
    SDFileUploadComponent,
    SDFormFieldComponent,
    SDFormFieldLabelComponent,
    StudiesComponent,
    TermsComponent,
    FiltersComponent,
    SearchResultComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    ColorPickerModule,
    CovalentTextEditorModule,
    FileDropModule,
    FlexLayoutModule,
    FormlyMaterialModule,
    FormlyModule.forRoot(),
    HttpClientModule,
    MarkdownModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatTableModule,
    MatToolbarModule,
    NgProgressModule,
    ReactiveFormsModule,
    RoutingModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
