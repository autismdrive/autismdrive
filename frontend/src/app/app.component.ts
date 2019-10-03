import { Component, OnInit } from '@angular/core';
import { ActivationEnd, ActivationStart, Router } from '@angular/router';
import { User } from './_models/user';
import { AuthenticationService } from './_services/api/authentication-service';
import {ApiService} from './_services/api/api.service';
import {GoogleAnalyticsService} from './google-analytics.service';
import {ConfigService} from './_services/config.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'star-drive';
  hideHeader = false;
  currentUser: User;

  public constructor(
    private authenticationService: AuthenticationService,
    private api: ApiService,
    private router: Router,
    private googleAnalyticsService: GoogleAnalyticsService,
    private configService: ConfigService
  ) {
    this.googleAnalyticsService.init();
    this.router.events.subscribe((e) => {
      if (e instanceof ActivationStart || e instanceof ActivationEnd) {
        if (e.snapshot && e.snapshot.data) {
          const data = e.snapshot.data;
          this.hideHeader = !!data.hideHeader;
        }
      }
    });
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  ngOnInit() {
  }

}
