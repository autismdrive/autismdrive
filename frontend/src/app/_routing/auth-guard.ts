import {Injectable} from '@angular/core';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot } from '@angular/router';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/authentication/authentication-service';

@Injectable({providedIn: 'root'})
export class AuthGuard  {
  private currentUser: User;

  constructor(private router: Router, private authenticationService: AuthenticationService) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (!this.currentUser) {
      console.log('On AuthGuard, and there is no user, sending to login!');
      this.router.navigate(['/login'], {queryParams: {returnUrl: state.url}});
      return false;
    } else {
      return true;
    }
  }
}
