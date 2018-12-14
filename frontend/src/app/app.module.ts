import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import {
  MatButtonModule,
  MatCardModule,
  MatIconModule,
  MatProgressBarModule,
  MatTableModule,
  MatToolbarModule,
  MatFormFieldModule
} from '@angular/material';
import { BrowserModule } from '@angular/platform-browser';
import { FileDropModule } from 'ngx-file-drop';
import { NgProgressModule } from 'ngx-progressbar';
import { ApiService } from './api.service';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { EnrollComponent } from './enroll/enroll.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { SDFileUploadComponent } from './forms/file-upload/file-upload.component';
import { SDFormFieldLabelComponent } from './forms/form-field-label/form-field-label.component';
import { SDFormFieldComponent } from './forms/form-field/form-field.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { LogoComponent } from './logo/logo.component';
import { ProfileComponent } from './profile/profile.component';
import { RegisterComponent } from './register/register.component';
import { ResourcesComponent } from './resources/resources.component';
import { StudiesComponent } from './studies/studies.component';
import { TermsComponent } from './terms/terms.component';

@NgModule({
  declarations: [
    AppComponent,
    EnrollComponent,
    ForgotPasswordComponent,
    HomeComponent,
    LoginComponent,
    LogoComponent,
    ProfileComponent,
    RegisterComponent,
    ResourcesComponent,
    SDFileUploadComponent,
    SDFormFieldComponent,
    SDFormFieldLabelComponent,
    StudiesComponent,
    TermsComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    FlexLayoutModule,
    HttpClientModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatProgressBarModule,
    MatIconModule,
    MatTableModule,
    MatToolbarModule,
    NgProgressModule,
    FileDropModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
