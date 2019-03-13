import { Component, OnInit } from '@angular/core';
import { ActivationEnd, ActivationStart, Router } from '@angular/router';
import { ApiService } from './services/api/api.service';
import { User } from './user';
import { IntervalService } from './services/interval/interval.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'star-drive';
  hideHeader = false;
  user: User = null;
  timeLeftInSession = 0;

  public constructor(
    private api: ApiService,
    private router: Router,
    private intervalService: IntervalService
  ) {

    this.router.events.subscribe((e) => {
      if (e instanceof ActivationStart || e instanceof ActivationEnd) {
        if (e.snapshot && e.snapshot.data) {
          const data = e.snapshot.data;
          this.hideHeader = !!data.hideHeader;
        }
      }
    });

    this.api.getSession().subscribe(userProps => {
      this.user = new User(userProps);
    });

    const numMinutes = 1;
    this.intervalService.setInterval(() => {
      // Update seconds
      this.timeLeftInSession -= 1000;

      // Check status every numMinutes
      if ((this.timeLeftInSession % (numMinutes * 60 * 1000)) < 1000) {
        this.checkStatus();
      }
    }, 1000);

  }

  ngOnInit() {
  }

  goLogout($event: MouseEvent) {
    $event.preventDefault();
    localStorage.setItem('prev_url', this.router.url);
    this.api.closeSession().subscribe();
    this.user = null;
    this.router.navigate(['logout']);
  }

  checkStatus() {
    const token = localStorage.getItem('token');

    if (token) {
      this.api.getSessionStatus().subscribe((timestamp: number) => {
        const now = new Date();
        const exp = new Date(timestamp * 1000);
        const msLeft: number = exp.getTime() - now.getTime();
        const loggedOut = (timestamp <= 0) || (msLeft <= 0);
        this.timeLeftInSession = msLeft;

        if (loggedOut) {
          this.api.closeSession().subscribe((_: any) => {
            this.intervalService.clearInterval();
            this.user = null;
            this.router.navigate(['timedout']);
          });
        } else {
          this.api.getSession().subscribe(userProps => {
            this.user = new User(userProps);
          });
        }
      });
    }
  }

  isLoggedIn() {
    return this.user && this.user.email;
  }
}
