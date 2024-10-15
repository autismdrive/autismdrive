import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';
import {ParticipantRelationship} from '@models/participantRelationship';
import {User} from '@models/user';
import {UserMeta} from '@models/user_meta';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

/**
 * Provides some messaging based on the profile meta information, this should be displayed
 * after someone completes the profile meta-data form, but before they have created a participant.
 * In some cases this may be as far as a user can go.
 */
@Component({
  selector: 'app-profile-meta',
  templateUrl: './profile_meta.component.html',
  styleUrls: ['./profile_meta.component.scss'],
})
export class ProfileMetaComponent {
  @Input()
  user: User;
  @Input()
  meta: UserMeta;

  relationships = ParticipantRelationship;

  constructor(
    private authenticationService: AuthenticationService,
    private api: ApiService,
    private router: Router,
  ) {}

  goFlow($event) {
    $event.preventDefault();
    this.router.navigate(['terms', this.meta.self_relationship]);
  }
}
