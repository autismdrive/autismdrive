import { Component, OnInit } from '@angular/core';
import { ActivationEnd, ActivationStart, Router } from '@angular/router';
import { User } from './_models/user';
import { AuthenticationService } from './_services/api/authentication-service';
import {ApiService} from './_services/api/api.service';
import {Status} from './_models/status';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'star-drive';
  hideHeader = false;
  currentUser: User;
  systemStatus: Status;

  public constructor(
    private authenticationService: AuthenticationService,
    private api: ApiService,
    private router: Router,
  ) {
    this.router.events.subscribe((e) => {
      if (e instanceof ActivationStart || e instanceof ActivationEnd) {
        if (e.snapshot && e.snapshot.data) {
          const data = e.snapshot.data;
          this.hideHeader = !!data.hideHeader;
        }
      }
    });
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.api.serverStatus.subscribe(s => this.systemStatus = s);
  }

  ngOnInit() {
  }

}
