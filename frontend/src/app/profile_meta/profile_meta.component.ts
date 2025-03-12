import {NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {RouterModule} from '@angular/router';
import {ParticipantRelationship} from '@models/participantRelationship';
import {User} from '@models/user';
import {UserMeta} from '@models/user_meta';
import {FlexModule} from '@ngbracket/ngx-layout';

/**
 * Provides some messaging based on the profile meta information, this should be displayed
 * after someone completes the profile meta-data form, but before they have created a participant.
 * In some cases this may be as far as a user can go.
 */
@Component({
  standalone: true,
  selector: 'app-profile-meta',
  templateUrl: './profile_meta.component.html',
  styleUrls: ['./profile_meta.component.scss'],
  imports: [FlexModule, NgIf, MatButtonModule, RouterModule],
})
export class ProfileMetaComponent {
  @Input() user: User;
  @Input() meta: UserMeta;

  relationships = ParticipantRelationship;

  constructor() {}

}
