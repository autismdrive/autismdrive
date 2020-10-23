import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/authentication/authentication-service';
import { User } from '../_models/user';


@Injectable({ providedIn: 'root' })
export class RoleGuard implements CanActivate {

  private currentUser: User;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    const roles = route.data['roles'] as Array<string>;

    if (!this.currentUser) {
      this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
      return false;
    } else if (!roles.includes(this.currentUser.role)) {
      this.router.navigate(['/profile']);
      return false;
    } else {
      return true;
    }
  }
}
