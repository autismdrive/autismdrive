import {Component, Input, OnInit} from '@angular/core';
import { User } from '../_models/user';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {ApiService} from '../_services/api/api.service';
import {Router} from '@angular/router';
import {Flow} from '../_models/flow';
import {UserMeta} from '../_models/user_meta';

@Component({
  selector: 'app-meta',
  templateUrl: './meta.component.html',
  styleUrls: ['./meta.component.scss']
})
export class MetaComponent implements OnInit {
  user: User;

  @Input()
  flow: Flow;
  meta: UserMeta;

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router
  ) {
        this.authenticationService.currentUser.subscribe(
            user => {
            this.user = user;
            }, error1 => {
              console.error(error1);
              this.user = null;
            });
    }

  ngOnInit(): void {
  }

  goProfile($event) {
    $event.preventDefault();
    this.router.navigate(['profile']);
  }

  goStudies($event) {
    $event.preventDefault();
    this.router.navigate(['studies']);
  }

  goResources($event) {
    $event.preventDefault();
    this.router.navigate(['search']);
  }



}
