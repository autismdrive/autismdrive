import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from '../_services/api/authentication-service';
import {map} from 'rxjs/operators';
import {User} from '../_models/user';


@Injectable({ providedIn: 'root' })
export class AdminGuard implements CanActivate {

  private currentUser: User;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
      if (!this.currentUser) {
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
        return false;
      } else if (this.currentUser.role !== 'admin') {
        this.router.navigate(['/profile']);
        return false;
      } else {
        return true;
      }
  }
}
