import {effect, Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Router, RouterStateSnapshot} from '@angular/router';
import {User} from '@app/shared/models/user';
import {AuthenticationService} from '@app/shared/services/authentication/authentication-service';

@Injectable({providedIn: 'root'})
export class AuthGuard {
  private currentUser: User;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService,
  ) {
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
    });
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (!this.currentUser) {
      this.router.navigate(['/login'], {queryParams: {returnUrl: state.url}});
      return false;
    } else {
      return true;
    }
  }
}
