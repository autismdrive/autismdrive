import {Component, OnInit} from '@angular/core';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {ApiService} from '../_services/api/api.service';
import {Router} from '@angular/router';
import {UserMeta} from '../_models/user_meta';
import {ParticipantRelationship} from '../_models/participantRelationship';

/**
 * Loads some metadata about the current user that we can use to suggest an appropriate flow
 * or other alternative path as they progress through the application.
 */
@Component({
  selector: 'app-meta',
  templateUrl: './meta.component.html',
  styleUrls: ['./meta.component.scss']
})
export class MetaComponent implements OnInit {
  user: User;
  meta: UserMeta;
  relationships = ParticipantRelationship;

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router
  ) {
    this.meta = this.getMockMeta();
    console.log('This.meta', this.meta);
    this.authenticationService.currentUser.subscribe(user => {
      this.user = user;
      /*
      this.api.getUserMeta(user.id).subscribe( meta => {
        this.meta = meta;
      }, error1 => {
        console.error(error1);
        this.meta = null;
      });
      */
    }, error1 => {
      console.error(error1);
      this.user = null;
    });
    }

  getMockMeta() {
    const meta = new UserMeta({});
    meta.self_relationship = null;

    return meta;
  }

  ngOnInit(): void {
    // this.meta = new UserMeta({});
    // this.meta = this.getMockMeta();
  }

  goFlow($event) {
    $event.preventDefault();
    this.router.navigate(['terms', this.meta.self_relationship]);
  }

}
