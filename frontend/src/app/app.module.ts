import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormioModule } from 'angular-formio';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule, MatToolbarModule} from '@angular/material';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ApiService } from './api.service';
import { LoginComponent } from './login/login.component';
import { LogoComponent } from './logo/logo.component';
import { RegisterComponent } from './register/register.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    LogoComponent,
    RegisterComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    FormioModule,
    HttpClientModule,
    MatIconModule,
    MatToolbarModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
