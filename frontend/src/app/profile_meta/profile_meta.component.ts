import {Component, Input, OnInit} from '@angular/core';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {ApiService} from '../_services/api/api.service';
import {Router} from '@angular/router';
import {UserMeta} from '../_models/user_meta';
import {ParticipantRelationship} from '../_models/participantRelationship';

/**
 * Provides some messaging based on the profile meta information, this should be displayed
 * after someone completes the profile meta-data form, but before they have created a participant.
 * In some cases this may be as far as a user can go.
 */
@Component({
  selector: 'app-profile-meta',
  templateUrl: './profile_meta.component.html',
  styleUrls: ['./profile_meta.component.scss']
})
export class ProfileMetaComponent implements OnInit {

  @Input()
  user: User;
  @Input()
  meta: UserMeta;

  relationships = ParticipantRelationship;

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router
  ) {
  }

  ngOnInit(): void {
  }

  goFlow($event) {
    $event.preventDefault();
    this.router.navigate(['terms', this.meta.self_relationship]);
  }

}
