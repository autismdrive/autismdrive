import { NgModule } from '@angular/core';
import { RouterModule, Routes, UrlSegment } from '@angular/router';
import { AdminHomeComponent } from '../admin-home/admin-home.component';
import { EnrollComponent } from '../enroll/enroll.component';
import { FlowCompleteComponent } from '../flow-complete/flow-complete.component';
import { FlowComponent } from '../flow/flow.component';
import { ForgotPasswordComponent } from '../forgot-password/forgot-password.component';
import { HomeComponent } from '../home/home.component';
import { LoginComponent } from '../login/login.component';
import { LogoutComponent } from '../logout/logout.component';
import { PasswordResetComponent } from '../password-reset/password-reset.component';
import { ProfileComponent } from '../profile/profile.component';
import { QuestionnaireDataViewComponent } from '../questionnaire-data-view/questionnaire-data-view.component';
import { RegisterComponent } from '../register/register.component';
import { ResourceDetailComponent } from '../resource-detail/resource-detail.component';
import { ResourceFormComponent } from '../resource-form/resource-form.component';
import { ResourcesComponent } from '../resources/resources.component';
import { SearchComponent } from '../search/search.component';
import { StudiesComponent } from '../studies/studies.component';
import { StudyDetailComponent } from '../study-detail/study-detail.component';
import { TermsComponent } from '../terms/terms.component';
import { UserAdminComponent } from '../user-admin/user-admin.component';
import { UserAdminDetailsComponent } from '../user-admin-details/user-admin-details.component';
import { TimedoutComponent } from '../timed-out/timed-out.component';
import { AdminGuard } from './admin-guard';
import { AuthGuard } from './auth-guard';

export function searchFilterMatcher(url: UrlSegment[]) {
  if (
    (url.length === 2) &&
    (url[0].path === ('search')) &&
    (url[1].path === ('filter'))
  ) {
    return { consumed: url };
  }
  return null;
}

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, data: { title: 'Welcome STAR Drive' } },
  { path: 'enroll', component: EnrollComponent, data: { title: 'Enroll in a STAR Drive Study' } },
  { path: 'forgot-password', component: ForgotPasswordComponent, data: { title: 'Log in to STAR Drive', hideHeader: true } },
  { path: 'login', component: LoginComponent, data: { title: 'Log in to STAR Drive', hideHeader: true } },
  {
    path: 'reset_password/:email_token', component: PasswordResetComponent,
    data: { title: 'Reset your STAR Drive password', hideHeader: true }
  },
  { path: 'profile', component: ProfileComponent, data: { title: 'Your STAR Drive Account' }, canActivate: [AuthGuard] },
  { path: 'flow/complete', component: FlowCompleteComponent, data: { title: 'Enrollment application complete' }, canActivate: [AuthGuard] },
  { path: 'flow/:flowName/:participantId', component: FlowComponent, data: { title: 'Your STAR Drive Account' }, canActivate: [AuthGuard] },
  { path: 'register', component: RegisterComponent, data: { title: 'Create a STAR Drive Account', hideHeader: true } },
  { path: 'event/:resourceId', component: ResourceDetailComponent, data: { title: 'Event Details' } },
  { path: 'location/:resourceId', component: ResourceDetailComponent, data: { title: 'Location Details' } },
  { path: 'resources', component: ResourcesComponent, data: { title: 'View STAR Drive Trainings & Resources' } },
  { path: 'resource/:resourceId', component: ResourceDetailComponent, data: { title: 'Resource Details' } },
  { path: 'resource/:resourceId/edit', component: ResourceFormComponent, data: { title: 'Edit Resource' }, canActivate: [AdminGuard] },
  { path: 'resources/add', component: ResourceFormComponent, data: { title: 'Add Resource' }, canActivate: [AdminGuard] },
  { path: 'studies', component: StudiesComponent, data: { title: 'Create a STAR Drive Account' } },
  { path: 'study/:studyId', component: StudyDetailComponent, data: { title: 'Study Details' } },
  { path: 'terms', component: TermsComponent, data: { title: 'Agree to Terms and Conditions for a STAR Drive Account', hideHeader: true } },
  { path: 'logout', component: LogoutComponent, data: { title: 'You have been logged out.', hideHeader: true } },
  { path: 'timedout', component: TimedoutComponent, data: { title: 'Your session has timed out.', hideHeader: true } },
  { path: 'search', component: SearchComponent, data: { title: 'Search' } },
  { path: 'search/:query', component: SearchComponent, data: { title: 'Search Resources' } },
  { matcher: searchFilterMatcher, component: SearchComponent, data: { title: 'Search' } },
  { path: 'admin', component: AdminHomeComponent, data: { title: 'Admin Home' }, canActivate: [AdminGuard] },
  { path: 'admin/data', component: QuestionnaireDataViewComponent, data: { title: 'Data Admin' }, canActivate: [AdminGuard] },
  { path: 'admin/user', component: UserAdminComponent, data: { title: 'User Admin' }, canActivate: [AdminGuard] },
  { path: 'admin/user/:userId', component: UserAdminDetailsComponent, data: { title: 'User Admin Details' }, canActivate: [AdminGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    useHash: true,
    scrollPositionRestoration: 'enabled'
  })],
  exports: [RouterModule]
})
export class RoutingModule { }
