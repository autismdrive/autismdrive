import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EnrollComponent } from '../enroll/enroll.component';
import { ForgotPasswordComponent } from '../forgot-password/forgot-password.component';
import { HomeComponent } from '../home/home.component';
import { LoginComponent } from '../login/login.component';
import { PasswordResetComponent } from '../password-reset/password-reset.component';
import { ProfileComponent } from '../profile/profile.component';
import { RegisterComponent } from '../register/register.component';
import { ResourcesComponent } from '../resources/resources.component';
import { StudiesComponent } from '../studies/studies.component';
import { TermsComponent } from '../terms/terms.component';
import { ResourceDetailComponent } from '../resource-detail/resource-detail.component';
import { StudyDetailComponent } from '../study-detail/study-detail.component';
import { TrainingDetailComponent } from '../training-detail/training-detail.component';
import { QuestionnaireStepComponent } from '../questionnaire-step/questionnaire-step.component';
import { FlowComponent } from '../flow/flow.component';
import { TimedoutComponent } from '../timed-out/timed-out.component';
import { LogoutComponent } from '../logout/logout.component';
import { FlowCompleteComponent } from '../flow-complete/flow-complete.component';
import {AuthGuard} from './auth-guard';

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
  { path: 'flow/complete', component: FlowCompleteComponent, data: { title: 'Enrollment application complete' } , canActivate: [AuthGuard]},
  { path: 'flow/:flowName/:participantId', component: FlowComponent, data: { title: 'Your STAR Drive Account' } , canActivate: [AuthGuard]},
  { path: 'register', component: RegisterComponent, data: { title: 'Create a STAR Drive Account', hideHeader: true } },
  { path: 'resources', component: ResourcesComponent, data: { title: 'View STAR Drive Trainings & Resources' } },
  { path: 'resource/:resourceId', component: ResourceDetailComponent, data: { title: 'Resource Details' } },
  { path: 'studies', component: StudiesComponent, data: { title: 'Create a STAR Drive Account' } },
  { path: 'study/:studyId', component: StudyDetailComponent, data: { title: 'Study Details' } },
  { path: 'terms', component: TermsComponent, data: { title: 'Agree to Terms and Conditions for a STAR Drive Account', hideHeader: true } },
  { path: 'logout', component: LogoutComponent, data: { title: 'You have been logged out.', hideHeader: true } },
  { path: 'timedout', component: TimedoutComponent, data: { title: 'Your session has timed out.', hideHeader: true } },
  { path: 'training/:trainingId', component: TrainingDetailComponent, data: { title: 'Training Details' } },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    useHash: true,
    scrollPositionRestoration: 'enabled'
  })],
  exports: [RouterModule]
})
export class RoutingModule { }
