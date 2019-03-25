import { Component, HostBinding, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { fadeTransition } from '../_animations/animations';

@Component({
  selector: 'app-timedout',
  templateUrl: './timed-out.component.html',
  styleUrls: ['./timed-out.component.scss'],
  animations: [fadeTransition()]
})
export class TimedoutComponent implements OnInit {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(
    private router: Router
  ) {
  }

  ngOnInit() { }

  goHome() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['']);
  }
}
