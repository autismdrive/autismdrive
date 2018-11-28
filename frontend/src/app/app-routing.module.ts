import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { EnrollComponent } from './enroll/enroll.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { RegisterComponent } from './register/register.component';
import { ResourcesComponent } from './resources/resources.component';
import { StudiesComponent } from './studies/studies.component';
import { TermsComponent } from './terms/terms.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, data: { title: 'Welcome STAR Drive' } },
  { path: 'enroll', component: EnrollComponent, data: { title: 'Enroll in a STAR Drive Study' } },
  { path: 'forgot-password', component: ForgotPasswordComponent, data: { title: 'Log in to STAR Drive', hideHeader: true } },
  { path: 'login', component: LoginComponent, data: { title: 'Log in to STAR Drive', hideHeader: true } },
  { path: 'profile', component: ProfileComponent, data: { title: 'Your STAR Drive Account' } },
  { path: 'register', component: RegisterComponent, data: { title: 'Create a STAR Drive Account', hideHeader: true } },
  { path: 'resources', component: ResourcesComponent, data: { title: 'View STAR Drive Trainings & Resources' } },
  { path: 'studies', component: StudiesComponent, data: { title: 'Create a STAR Drive Account' } },
  { path: 'terms', component: TermsComponent, data: { title: 'Agree to Terms and Conditions for a STAR Drive Account', hideHeader: true } },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
