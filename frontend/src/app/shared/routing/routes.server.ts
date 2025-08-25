import {RenderMode, ServerRoute} from '@angular/ssr';

/**
 * Server-side routes for the Autism DRIVE application.
 * ----------------------------------------------------------------------------
 * Defines the routes for the application, including static pre-rendered and
 * dynamic server-rendered components.
 *
 * Routes are sorted by specificity ("first-match-wins" strategy):
 * 1. Static paths
 * 2. Empty path (i.e., the default route)
 * 3. Routes with parameters
 * 4. Routes with wildcards (e.g., catch-all route)
 */
export const serverRoutes: ServerRoute[] = [
  /*****************************
   *   1. Static path routes   *
   *****************************/

  // Static public content (rendered at build time)
  {path: 'about', renderMode: RenderMode.Prerender},
  {path: 'forgot-password', renderMode: RenderMode.Prerender},
  {path: 'login', renderMode: RenderMode.Prerender},
  {path: 'logout', renderMode: RenderMode.Prerender},
  {path: 'register', renderMode: RenderMode.Prerender},
  {path: 'timedout', renderMode: RenderMode.Prerender},

  // Dynamically-rendered public content (rendered on user/search engine request)
  {path: 'covid19-resources', renderMode: RenderMode.Server},
  {path: 'home', renderMode: RenderMode.Server},
  {path: 'search', renderMode: RenderMode.Server},
  {path: 'studies', renderMode: RenderMode.Server},
  {path: 'uva-education', renderMode: RenderMode.Server},

  // Logged-in routes containing user-specific data
  {path: 'admin', renderMode: RenderMode.Server},
  {path: 'admin/data-admin', renderMode: RenderMode.Server},
  {path: 'admin/email-log', renderMode: RenderMode.Server},
  {path: 'admin/import-export-status', renderMode: RenderMode.Server},
  {path: 'admin/participant-admin', renderMode: RenderMode.Server},
  {path: 'admin/taxonomy-admin', renderMode: RenderMode.Server},
  {path: 'admin/user-admin', renderMode: RenderMode.Server},
  {path: 'flow/complete', renderMode: RenderMode.Server},
  {path: 'mirrored', renderMode: RenderMode.Server},
  {path: 'profile', renderMode: RenderMode.Server},
  {path: 'resources/add', renderMode: RenderMode.Server},
  {path: 'studies/add', renderMode: RenderMode.Server},

  /*****************************
   *    2. Empty path route    *
   *****************************/

  {path: '', renderMode: RenderMode.Server},

  /*****************************
   * 3. Routes with parameters *
   *****************************/

  // Static public content (rendered at build time)
  {path: 'terms/:relationship', renderMode: RenderMode.Prerender},

  // Dynamically-rendered public content (rendered on user/search engine request)
  {path: 'covid19-resources/:category', renderMode: RenderMode.Server},
  {path: 'event/:resourceId', renderMode: RenderMode.Server},
  {path: 'location/:resourceId', renderMode: RenderMode.Server},
  {path: 'resource/:resourceId', renderMode: RenderMode.Server},
  {path: 'search/:query', renderMode: RenderMode.Server}, // Dynamically rendered
  {path: 'studies/:studyStatus', renderMode: RenderMode.Server},
  {path: 'studies/:studyStatus/:age', renderMode: RenderMode.Server},
  {path: 'study/:studyId', renderMode: RenderMode.Server},

  // Admin & content-management routes
  {path: ':resourceType/:resourceId/edit', renderMode: RenderMode.Server},
  {path: 'admin/user/:userId', renderMode: RenderMode.Server},
  {path: 'study/edit/:studyId', renderMode: RenderMode.Server},

  // Logged-in user routes
  {path: 'flow/:flowName/:participantId', renderMode: RenderMode.Server},
  {path: 'session/:token', renderMode: RenderMode.Server},

  /*****************************
   * 4. Routes with wildcards *
   *****************************/

  // Catch-all route for 404 errors
  {path: '**', renderMode: RenderMode.Server, status: 404},
];
