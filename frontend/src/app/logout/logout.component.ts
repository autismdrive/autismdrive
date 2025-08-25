import {Component, HostBinding, OnInit} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {RouterModule} from '@angular/router';
import {fadeTransition} from '@animations/animations';
import {LogoComponent} from '@app/logo/logo.component';
import {FlexModule} from '@ngbracket/ngx-layout';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  standalone: true,
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss'],
  animations: [fadeTransition()],
  imports: [FlexModule, LogoComponent, RouterModule, MatButtonModule],
})
export class LogoutComponent implements OnInit {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(private authenticationService: AuthenticationService) {}

  ngOnInit() {
    this.authenticationService.logout();
  }
}
