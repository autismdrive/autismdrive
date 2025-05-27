import {effect, Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Router, RouterStateSnapshot} from '@angular/router';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';

@Injectable({providedIn: 'root'})
export class NotMirroredGuard {
  // Checks to see if the server we are connected to is running in a mirroring mode.  If so
  // prevent users from taking actions that might cause data issues later on.

  constructor(
    private router: Router,
    private appEnvironmentService: AppEnvironmentService,
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.appEnvironmentService.props() && this.appEnvironmentService.mirroring) {
      this.router.navigate(['/mirrored']);
      return false;
    } else {
      return true;
    }
  }
}
