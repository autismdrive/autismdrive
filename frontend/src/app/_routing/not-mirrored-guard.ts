import {Injectable} from '@angular/core';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot } from '@angular/router';
import {ConfigService} from '../_services/config/config.service';

@Injectable({providedIn: 'root'})
export class NotMirroredGuard  {
  // Checks to see if the server we are connected to is running in a mirroring mode.  If so
  // prevent users from taking actions that might cause data issues later on.

  constructor(private router: Router, private configService: ConfigService) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.configService && this.configService.mirroring) {
      this.router.navigate(['/mirrored']);
      return false;
    } else {
      return true;
    }
  }
}
