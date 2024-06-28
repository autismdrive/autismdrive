import {Component, HostBinding} from '@angular/core';
import {Router} from '@angular/router';
import {fadeTransition} from '../_animations/animations';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss'],
  animations: [fadeTransition()],
})
export class LogoutComponent {
  @HostBinding('@fadeTransition')
  title: string;

  constructor(
    private api: ApiService,
    private router: Router,
  ) {}

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }
}
