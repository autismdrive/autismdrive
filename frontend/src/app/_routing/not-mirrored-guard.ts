import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/api/authentication-service';
import {ApiService} from '../_services/api/api.service';
import {Status} from '../_models/status';


@Injectable({ providedIn: 'root' })
export class NotMirroredGuard implements CanActivate {
  // Checks to see if the server we are connected to is running in a mirroring mode.  If so
  // prevent users from taking actions that might cause data issues later on.

  private serverStatus: Status;

  constructor(
    private router: Router,
    private apiService: ApiService
  ) {
    this.apiService.serverStatus.subscribe(s => this.serverStatus = s);
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.serverStatus && this.serverStatus.mirroring) {
      this.router.navigate(['/mirrored']);
      return false;
    } else {
      return true;
    }
  }
}
