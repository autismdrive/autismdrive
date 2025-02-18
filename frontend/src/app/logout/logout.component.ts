import {Component, HostBinding, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {fadeTransition} from '@animations/animations';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  standalone: true,
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss'],
  animations: [fadeTransition()],
})
export class LogoutComponent implements OnInit {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(private authenticationService: AuthenticationService) {}

  ngOnInit() {
    this.authenticationService.logout();
  }
}
