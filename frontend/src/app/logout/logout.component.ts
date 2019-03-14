import { Component, HostBinding, OnInit } from '@angular/core';
import { fadeTransition } from '../_animations/animations';
import { ApiService } from '../_services/api/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss'],
  animations: [fadeTransition()]
})
export class LogoutComponent implements OnInit {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(
    private api: ApiService,
    private router: Router
  ) {
  }

  ngOnInit() { }

  goHome() {
    const prevUrl = localStorage.getItem('prev_url') || '/';
    this.router.navigateByUrl(prevUrl);
    localStorage.clear();
    sessionStorage.clear();
  }
}
