import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect, OnInit, signal, WritableSignal} from '@angular/core';
import {AbstractControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatLineModule} from '@angular/material/core';
import {MatListModule} from '@angular/material/list';
import {MatTabsModule} from '@angular/material/tabs';
import {ActivatedRoute, RouterModule} from '@angular/router';
import {FavoriteResourcesComponent} from '@app/favorite-resources/favorite-resources.component';
import {FavoriteTopicsComponent} from '@app/favorite-topics/favorite-topics.component';
import {LoadingComponent} from '@app/loading/loading.component';
import {ParticipantProfileComponent} from '@app/participant-profile/participant-profile.component';
import {ProfileMetaComponent} from '@app/profile-meta/profile-meta.component';
import {Participant} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {Resource} from '@models/resource';
import {Study} from '@models/study';
import {StudyUser} from '@models/study_user';
import {User} from '@models/user';
import {UserMeta} from '@models/user_meta';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyFormOptions, FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {firstValueFrom} from 'rxjs';

export const profileFormFields = [
  {
    validators: {
      fieldMatch: {
        expression: (control: AbstractControl) => {
          const {self_participant, guardian, professional, interested} = control.value;

          // at least one checkbox should be selected.
          return !(!self_participant && !guardian && !professional && !interested);
        },
        message: 'Please select at least one option.',
      },
    },
    wrappers: ['group-validation'],
    fieldGroup: [
      {
        key: 'self_participant',
        type: 'checkbox',
        props: {label: 'I am autistic/I have autism', indeterminate: false, class: 'self_participant'},
      },
      {
        key: 'self_has_guardian',
        type: 'radio',
        props: {
          label: 'Do you have a legal guardian?',
          options: [
            {value: true, label: 'Yes', id: '1'},
            {value: false, label: 'No', id: '2'},
          ],
        },
        expressionProperties: {
          'props.required': 'model.self_participant',
        },
        hideExpression: '!model.self_participant',
      },
      {
        key: 'guardian',
        type: 'checkbox',
        className: 'guardian',
        props: {label: 'I am the parent/legal guardian of someone with autism', indeterminate: false},
      },
      {
        key: 'guardian_has_dependent',
        type: 'radio',
        className: 'guardian_has_dependent',
        props: {
          label: 'Are you their legal guardian?',
          options: [
            {value: true, label: 'Yes', id: '3'},
            {value: false, label: 'No', id: '4'},
          ],
        },
        expressionProperties: {
          'props.required': 'model.guardian',
        },
        hideExpression: '!model.guardian',
      },
      {
        key: 'professional',
        type: 'checkbox',
        props: {label: 'I am a professional who works with the autism community', indeterminate: false},
      },
      {
        key: 'interested',
        type: 'checkbox',
        props: {
          label: 'None of the above, but I am interested in autism research and resources',
          indeterminate: false,
        },
      },
    ],
  },
];

enum ProfileState {
  NEEDS_USER = 'NEEDS_USER',
  NEEDS_META = 'NEEDS_META',
  NEEDS_PARTICIPANT = 'NEEDS_PARTICIPANT',
  HAS_PARTICIPANT = 'PARTICIPANT',
}

@Component({
  standalone: true,
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
  imports: [
    CommonModule,
    FavoriteResourcesComponent,
    FavoriteTopicsComponent,
    FlexModule,
    FormlyModule,
    LoadingComponent,
    MatButtonModule,
    MatCardModule,
    MatLineModule,
    MatListModule,
    MatTabsModule,
    ParticipantProfileComponent,
    ProfileMetaComponent,
    ReactiveFormsModule,
    RouterModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProfileComponent implements OnInit {
  loading: WritableSignal<boolean> = signal(true);
  profileState: WritableSignal<ProfileState> = signal(undefined);
  userRelationship: WritableSignal<ParticipantRelationship> = signal(undefined);

  user: User;
  userMeta: UserMeta;
  possibleStates = ProfileState;
  relationships = ParticipantRelationship;
  studyInquiries: StudyUser[];
  currentStudies: Study[];
  self: Participant;
  dependents: Participant[];
  favoriteResources: Resource[];
  selfPercentComplete: number;
  form = new FormGroup({});
  model = new UserMeta({});
  options: FormlyFormOptions = {};
  fields: FormlyFieldConfig[] = profileFormFields;

  userRelationshipMessages = Object.fromEntries([
    [
      this.relationships.SELF_PROFESSIONAL,
      `You indicated that you are a professional working in Autism research and treatment. Once your profile is complete we will be able to notify you about important updates.`,
    ],
    [
      this.relationships.SELF_INTERESTED,
      `Once your profile is complete we will be able to notify you about important updates.`,
    ],
    [
      this.relationships.SELF_PARTICIPANT,
      `Once your profile is complete, you'll be able to enroll in any relevant currently-running studies.`,
    ],
    [
      this.relationships.SELF_GUARDIAN,
      `Once your complete your profile and the profiles of your dependents, you'll be able to enroll them in any relevant currently-running studies.`,
    ],
  ]);

  constructor(
    public authenticationService: AuthenticationService,
    private api: ApiService,
    private route: ActivatedRoute,
  ) {
    this.route.queryParams.subscribe(params => {
      if (params.hasOwnProperty('meta')) {
        this.profileState.set(ProfileState.NEEDS_META);
      }
    });

    effect(async () => {
      this.user = this.authenticationService.currentUser();

      if (!this.user) {
        this.user = null;
        this.loading.set(false);
        return;
      }

      this.self = this.user.getSelf();
      this.dependents = this.user.getDependents();

      this.userMeta = await firstValueFrom(this.api.getUserMeta(this.user.id));
      this.loading.set(false);

      await this.refreshParticipants();
      this.studyInquiries = await firstValueFrom(this.api.getUserStudyInquiries(this.user.id));
      const all = await firstValueFrom(this.api.getStudies());
      this.currentStudies = all.filter(s => s.status === 'currently_enrolling');
      this.favoriteResources = this.user.user_favorites
        .filter(f => f.type === 'resource')
        .map(f => f.resource)
        .sort(a => a.id);

      this.profileState.set(this.getProfileState());
    });

    effect(() => {
      if (this.profileState() === ProfileState.HAS_PARTICIPANT) {
        // user has a participant profile.
        this.userRelationship.set(this.user.getSelf().relationship);
      } else {
        // user does not have a participant profile.
        this.userRelationship.set(undefined);
      }
    });
  }

  ngOnInit() {}

  async refreshParticipants() {
    if (this.user) {
      const u = await firstValueFrom(this.api.getUser(this.user.id));
      const newU = new User(u);
      this.self = newU.getSelf();
      this.dependents = newU.getDependents();
      if (newU.getSelf()) {
        const f = await firstValueFrom(this.api.getFlow(newU.getSelf().getFlowName(), newU.getSelf().id));
        this.selfPercentComplete = f.percentComplete();
      }
    }
  }

  getProfileState() {
    if (!this.user) {
      // can happen if user logs out from this page.
      return ProfileState.NEEDS_USER;
    } else if (this.userMeta === undefined) {
      return ProfileState.NEEDS_META;
    } else if (this.user.getSelf() === undefined) {
      return ProfileState.NEEDS_PARTICIPANT;
    } else {
      return ProfileState.HAS_PARTICIPANT;
    }
  }

  async createMeta() {
    if (this.form.valid) {
      this.model.id = this.user.id;
      this.userMeta = await firstValueFrom(this.api.addUserMeta(this.model));
    }
  }

  protected readonly ParticipantRelationship = ParticipantRelationship;
}
