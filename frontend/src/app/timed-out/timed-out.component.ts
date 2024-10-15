import {Component, HostBinding, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {fadeTransition} from '@animations/animations';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  selector: 'app-timedout',
  templateUrl: './timed-out.component.html',
  styleUrls: ['./timed-out.component.scss'],
  animations: [fadeTransition()],
})
export class TimedoutComponent implements OnInit {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService,
  ) {}

  ngOnInit() {
    this.authenticationService.logout();
  }

  goHome() {
    this.router.navigate(['']);
  }

  goLogin() {
    this.router.navigate(['/login']);
  }
}
