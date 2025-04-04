import {Routes} from '@angular/router';
import {AuthGuard} from './auth-guard';
import {NotMirroredGuard} from './not-mirrored-guard';
import {RoleGuard} from './role-guard';

export const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {
    path: 'home',
    loadComponent: () => import('../home/home.component').then(c => c.HomeComponent),
    data: {title: 'Welcome to Autism DRIVE'},
    canActivate: [NotMirroredGuard],
  },
  {
    path: 'uva-education',
    loadComponent: () => import('../uva-education/uva-education.component').then(c => c.UvaEducationComponent),
    data: {title: 'Autism DRIVE UVA Education'},
    canActivate: [NotMirroredGuard],
  },
  {
    path: 'about',
    loadComponent: () => import('../about/about.component').then(c => c.AboutComponent),
    data: {title: 'About Autism DRIVE'},
    canActivate: [NotMirroredGuard],
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('../forgot-password/forgot-password.component').then(c => c.ForgotPasswordComponent),
    data: {title: 'Log in to Autism DRIVE', hideHeader: true},
  },
  {
    path: 'login',
    loadComponent: () => import('../login/login.component').then(c => c.LoginComponent),
    data: {title: 'Log in to Autism DRIVE', hideHeader: true},
  },
  {
    path: 'reset_password/:role/:email_token',
    loadComponent: () => import('../password-reset/password-reset.component').then(c => c.PasswordResetComponent),
    data: {title: 'Reset your Autism DRIVE password', hideHeader: true},
  },
  {
    path: 'profile',
    loadComponent: () => import('../profile/profile.component').then(c => c.ProfileComponent),
    data: {title: 'Your Autism DRIVE Account'},
    canActivate: [AuthGuard, NotMirroredGuard],
  },
  {
    path: 'flow/complete',
    loadComponent: () => import('../flow-complete/flow-complete.component').then(c => c.FlowCompleteComponent),
    data: {title: 'Enrollment complete'},
    canActivate: [AuthGuard, NotMirroredGuard],
  },
  {
    path: 'flow/:flowName/:participantId',
    loadComponent: () => import('../flow/flow.component').then(c => c.FlowComponent),
    data: {title: 'Your Autism DRIVE Account'},
    canActivate: [AuthGuard, NotMirroredGuard],
  },
  {
    path: 'register',
    loadComponent: () => import('../register/register.component').then(c => c.RegisterComponent),
    data: {title: 'Create an Autism DRIVE Account', hideHeader: true},
  },
  {
    path: 'event/:resourceId',
    loadComponent: () => import('../resource-detail/resource-detail.component').then(c => c.ResourceDetailComponent),
    data: {title: 'Autism DRIVE Event Details'},
  },
  {
    path: 'location/:resourceId',
    loadComponent: () => import('../resource-detail/resource-detail.component').then(c => c.ResourceDetailComponent),
    data: {title: 'Autism DRIVE Location Details'},
  },
  {
    path: 'resource/:resourceId',
    loadComponent: () => import('../resource-detail/resource-detail.component').then(c => c.ResourceDetailComponent),
    data: {title: 'Autism DRIVE Resource Details'},
  },
  {
    path: ':resourceType/:resourceId/edit',
    loadComponent: () => import('../resource-form/resource-form.component').then(c => c.ResourceFormComponent),
    data: {title: 'Edit Resource', roles: ['admin', 'editor']},
    canActivate: [RoleGuard],
  },
  {
    path: 'resources/add',
    loadComponent: () => import('../resource-form/resource-form.component').then(c => c.ResourceFormComponent),
    data: {title: 'Add Resource', roles: ['admin', 'editor']},
    canActivate: [RoleGuard],
  },
  {
    path: 'covid19-resources',
    loadComponent: () =>
      import('../covid19-resources/covid19-resources.component').then(c => c.Covid19ResourcesComponent),
    data: {title: 'Autism DRIVE COVID-19 Resources'},
  },
  {
    path: 'covid19-resources/:category',
    loadComponent: () =>
      import('../covid19-resources/covid19-resources.component').then(c => c.Covid19ResourcesComponent),
    data: {title: 'Autism DRIVE COVID-19 Resources'},
  },
  {
    path: 'studies',
    loadComponent: () => import('../studies/studies.component').then(c => c.StudiesComponent),
    data: {title: 'Autism DRIVE Studies'},
  },
  {
    path: 'studies/add',
    loadComponent: () => import('../study-form/study-form.component').then(c => c.StudyFormComponent),
    data: {title: 'Create an Autism DRIVE Study', roles: ['admin']},
    canActivate: [RoleGuard],
  },
  {
    path: 'studies/:studyStatus',
    loadComponent: () => import('../studies/studies.component').then(c => c.StudiesComponent),
    data: {title: 'Autism DRIVE Studies'},
  },
  {
    path: 'studies/:studyStatus/:age',
    loadComponent: () => import('../studies/studies.component').then(c => c.StudiesComponent),
    data: {title: 'Autism DRIVE Studies'},
  },
  {
    path: 'study/:studyId',
    loadComponent: () => import('../study-detail/study-detail.component').then(c => c.StudyDetailComponent),
    data: {title: 'Autism DRIVE Study Details'},
  },
  {
    path: 'study/edit/:studyId',
    loadComponent: () => import('../study-form/study-form.component').then(c => c.StudyFormComponent),
    data: {title: 'Edit Study', roles: ['admin']},
    canActivate: [RoleGuard],
  },
  {
    path: 'terms/:relationship',
    loadComponent: () => import('../terms/terms.component').then(c => c.TermsComponent),
    data: {title: 'Agree to Terms and Conditions for an Autism DRIVE Account', hideHeader: true},
  },
  {
    path: 'logout',
    loadComponent: () => import('../logout/logout.component').then(c => c.LogoutComponent),
    data: {title: 'You have been logged out.', hideHeader: true},
  },
  {
    path: 'timedout',
    loadComponent: () => import('../timed-out/timed-out.component').then(c => c.TimedOutComponent),
    data: {title: 'Your session has timed out.', hideHeader: true},
  },
  {
    path: 'search',
    loadComponent: () => import('../search/search.component').then(c => c.SearchComponent),
    data: {title: 'Search Autism DRIVE'},
  },
  {
    path: 'search/:query',
    loadComponent: () => import('../search/search.component').then(c => c.SearchComponent),
    data: {title: 'Search Autism DRIVE Resources'},
  },
  {
    path: 'admin',
    loadComponent: () => import('../admin-home/admin-home.component').then(c => c.AdminHomeComponent),
    data: {title: 'Autism DRIVE Admin Home', roles: ['admin']},
    canActivate: [RoleGuard],
    children: [
      {path: '', redirectTo: 'data-admin', pathMatch: 'full'},
      {
        path: 'data-admin',
        loadComponent: () =>
          import('../questionnaire-data-view/questionnaire-data-view.component').then(
            c => c.QuestionnaireDataViewComponent,
          ),
        data: {title: 'Autism DRIVE Data Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
      {
        path: 'user-admin',
        loadComponent: () => import('../user-admin/user-admin.component').then(c => c.UserAdminComponent),
        data: {title: 'Autism DRIVE User Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
      {
        path: 'participant-admin',
        loadComponent: () =>
          import('../participant-admin/participant-admin.component').then(c => c.ParticipantAdminComponent),
        data: {title: 'Autism DRIVE Participant Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
      {
        path: 'taxonomy-admin',
        loadComponent: () => import('../taxonomy-admin/taxonomy-admin.component').then(c => c.TaxonomyAdminComponent),
        data: {title: 'Autism DRIVE Taxonomy Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
      {
        path: 'import-export-status',
        loadComponent: () => import('../admin-export/admin-export.component').then(c => c.AdminExportComponent),
        data: {title: 'Autism DRIVE Import/Export Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
      {
        path: 'email-log',
        loadComponent: () => import('../email-log-admin/email-log-admin.component').then(c => c.EmailLogAdminComponent),
        data: {title: 'Autism DRIVE Email Log Admin', roles: ['admin']},
        canActivate: [RoleGuard],
      },
    ],
  },
  {
    path: 'admin/user/:userId',
    loadComponent: () =>
      import('../user-admin-details/user-admin-details.component').then(c => c.UserAdminDetailsComponent),
    data: {title: 'User Admin Details', roles: ['admin', 'researcher']},
    canActivate: [RoleGuard],
  },
  {
    path: 'mirrored',
    loadComponent: () => import('../mirror/mirror.component').then(c => c.MirrorComponent),
    data: {title: 'Mirrored Server Details'},
  },
];
