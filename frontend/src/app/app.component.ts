import { Component, OnInit } from '@angular/core';
import { ActivationEnd, ActivationStart, Router } from '@angular/router';
import { ApiService } from './api.service';
import { User } from './user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'star-drive';
  hideHeader = false;
  session: User;

  public constructor(
    private api: ApiService,
    private router: Router
  ) {

    this.router.events.subscribe((e) => {
      if (e instanceof ActivationStart || e instanceof ActivationEnd) {
        if (e.snapshot && e.snapshot.data) {
          const data = e.snapshot.data;
          this.hideHeader = !!data.hideHeader;
        }
      }
    });

    this.api.getSession().subscribe(user => {
      this.session = user;
    }, error1 => {
      this.session = null;
    });
  }

  ngOnInit() {
  }

  goLogout($event) {
    $event.preventDefault();
    this.api.closeSession().subscribe(response => {
      this.router.navigate(['home']);
    });
  }
}
