import {NgModule} from '@angular/core';
import {RouterModule, Routes, UrlSegment} from '@angular/router';
import {AdminHomeComponent} from '../admin-home/admin-home.component';
import {AboutComponent} from '../about/about.component';
import {FlowCompleteComponent} from '../flow-complete/flow-complete.component';
import {FlowComponent} from '../flow/flow.component';
import {ForgotPasswordComponent} from '../forgot-password/forgot-password.component';
import {HomeComponent} from '../home/home.component';
import {LoginComponent} from '../login/login.component';
import {LogoutComponent} from '../logout/logout.component';
import {PasswordResetComponent} from '../password-reset/password-reset.component';
import {ProfileComponent} from '../profile/profile.component';
import {QuestionnaireDataViewComponent} from '../questionnaire-data-view/questionnaire-data-view.component';
import {RegisterComponent} from '../register/register.component';
import {ResourceDetailComponent} from '../resource-detail/resource-detail.component';
import {ResourceFormComponent} from '../resource-form/resource-form.component';
import {ResourcesComponent} from '../resources/resources.component';
import {SearchComponent} from '../search/search.component';
import {StudiesComponent} from '../studies/studies.component';
import {StudyDetailComponent} from '../study-detail/study-detail.component';
import {TermsComponent} from '../terms/terms.component';
import {UserAdminComponent} from '../user-admin/user-admin.component';
import {UserAdminDetailsComponent} from '../user-admin-details/user-admin-details.component';
import {TimedoutComponent} from '../timed-out/timed-out.component';
import {AdminGuard} from './admin-guard';
import {AuthGuard} from './auth-guard';
import {MirrorComponent} from '../mirror/mirror.component';
import {NotMirroredGuard} from './not-mirrored-guard';
import {AdminExportComponent} from '../admin-export/admin-export.component';

export function searchFilterMatcher(url: UrlSegment[]) {
  if (
    (url.length === 2) &&
    (url[0].path === ('search')) &&
    (url[1].path === ('filter'))
  ) {
    return {consumed: url};
  }
  return null;
}

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full', canActivate: [NotMirroredGuard]},
  {path: 'home', component: HomeComponent, data: {title: 'Welcome Autism DRIVE'}, canActivate: [NotMirroredGuard]},
  {
    path: 'about',
    component: AboutComponent,
    data: {title: 'Enroll in an Autism DRIVE Study'},
    canActivate: [NotMirroredGuard]
  },
  {
    path: 'forgot-password',
    component: ForgotPasswordComponent,
    data: {title: 'Log in to Autism DRIVE', hideHeader: true}
  },
  {path: 'login', component: LoginComponent, data: {title: 'Log in to Autism DRIVE', hideHeader: true}},
  {
    path: 'reset_password/:email_token', component: PasswordResetComponent,
    data: {title: 'Reset your Autism DRIVE password', hideHeader: true}
  },
  {
    path: 'profile',
    component: ProfileComponent,
    data: {title: 'Your Autism DRIVE Account'},
    canActivate: [AuthGuard, NotMirroredGuard]
  },
  {
    path: 'flow/complete',
    component: FlowCompleteComponent,
    data: {title: 'Enrollment application complete'},
    canActivate: [AuthGuard, NotMirroredGuard]
  },
  {
    path: 'flow/:flowName/:participantId',
    component: FlowComponent,
    data: {title: 'Your Autism DRIVE Account'},
    canActivate: [AuthGuard, NotMirroredGuard]
  },
  {path: 'register', component: RegisterComponent, data: {title: 'Create an Autism DRIVE Account', hideHeader: true}},
  {path: 'event/:resourceId', component: ResourceDetailComponent, data: {title: 'Event Details'}},
  {path: 'location/:resourceId', component: ResourceDetailComponent, data: {title: 'Location Details'}},
  {path: 'resources', component: ResourcesComponent, data: {title: 'View Autism DRIVE Trainings & Resources'}},
  {path: 'resource/:resourceId', component: ResourceDetailComponent, data: {title: 'Resource Details'}},
  {
    path: ':resourceType/:resourceId/edit',
    component: ResourceFormComponent,
    data: {title: 'Edit Resource'},
    canActivate: [AdminGuard]
  },
  {path: 'resources/add', component: ResourceFormComponent, data: {title: 'Add Resource'}, canActivate: [AdminGuard]},
  {path: 'studies', component: StudiesComponent, data: {title: 'Create an Autism DRIVE Account'}},
  {path: 'study/:studyId', component: StudyDetailComponent, data: {title: 'Study Details'}},
  {
    path: 'terms',
    component: TermsComponent,
    data: {title: 'Agree to Terms and Conditions for an Autism DRIVE Account', hideHeader: true}
  },
  {path: 'logout', component: LogoutComponent, data: {title: 'You have been logged out.', hideHeader: true}},
  {path: 'timedout', component: TimedoutComponent, data: {title: 'Your session has timed out.', hideHeader: true}},
  {path: 'search', component: SearchComponent, data: {title: 'Search'}},
  {path: 'search/:query', component: SearchComponent, data: {title: 'Search Resources'}},
  {matcher: searchFilterMatcher, component: SearchComponent, data: {title: 'Search'}},
  {path: 'admin', component: AdminHomeComponent, data: {title: 'Admin Home'}, canActivate: [AdminGuard]},
  {
    path: 'admin/data',
    component: QuestionnaireDataViewComponent,
    data: {title: 'Data Admin'},
    canActivate: [AdminGuard]
  },
  {path: 'admin/user', component: UserAdminComponent, data: {title: 'User Admin'}, canActivate: [AdminGuard]},
  {
    path: 'admin/user/:userId',
    component: UserAdminDetailsComponent,
    data: {title: 'User Admin Details'},
    canActivate: [AdminGuard]
  },
  {
    path: 'admin/export',
    component: AdminExportComponent,
    data: {title: 'Export/Import Status'},
    canActivate: [AdminGuard]
  },
  {path: 'mirrored', component: MirrorComponent, data: {title: 'Mirrored Server Details'}},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    useHash: true,
    scrollPositionRestoration: 'enabled'
  })],
  exports: [RouterModule]
})
export class RoutingModule {
}
