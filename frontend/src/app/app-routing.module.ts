import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, data: { title: 'Welcome STAR Drive' } },
  { path: 'login', component: LoginComponent, data: { title: 'Log in to STAR Drive', hideHeader: true } },
  { path: 'register', component: RegisterComponent, data: { title: 'Create a STAR Drive Account', hideHeader: true } },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
