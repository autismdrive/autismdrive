import {Component, OnInit} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {Participant} from '@models/participant';
import {ParticipantRelationship} from '@models/participantRelationship';
import {Resource} from '@models/resource';
import {Study} from '@models/study';
import {StudyUser} from '@models/study_user';
import {User} from '@models/user';
import {UserMeta} from '@models/user_meta';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

enum ProfileState {
  NEEDS_USER = 'NEEDS_USER',
  NEEDS_META = 'NEEDS_META',
  NEEDS_PARTICIPANT = 'NEEDS_PARTICIPANT',
  HAS_PARTICIPANT = 'PARTICIPANT',
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  user: User;
  userMeta: UserMeta;
  possibleStates = ProfileState;
  forceMetaFormState = false;
  relationships = ParticipantRelationship;
  loading = true;
  studyInquiries: StudyUser[];
  currentStudies: Study[];
  self: Participant;
  dependents: Participant[];
  favoriteResources: Resource[];
  selfPercentComplete: number;
  form = new FormGroup({});
  model = new UserMeta({});
  options: FormlyFormOptions = {};
  fields: FormlyFieldConfig[] = [
    {
      validators: {
        fieldMatch: {
          expression: control => {
            const {self_participant, guardian, professional, interested} = control.value;

            // at least one checkbox should be selected.
            if (!self_participant && !guardian && !professional && !interested) {
              return false;
            }
            return true;
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

  constructor(
    private authenticationService: AuthenticationService,
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    this.route.queryParams.subscribe(params => {
      console.log('Params', params);
      if (params.hasOwnProperty('meta')) {
        this.forceMetaFormState = true;
      }
    });

    this.authenticationService.currentUser.subscribe(
      user => {
        this.user = user;
        console.log(user);
        this.self = user.getSelf();
        this.dependents = user.getDependents();

        this.api.getUserMeta(user.id).subscribe(
          meta => {
            console.log('UserMeta', meta);
            this.userMeta = meta;
            this.loading = false;
          },
          error1 => {
            console.error(error1);
            this.loading = false;
          },
        );
      },
      error1 => {
        console.error(error1);
        this.user = null;
        this.loading = false;
      },
    );
  }

  ngOnInit() {
    this.refreshParticipants();
    this.api.getUserStudyInquiries(this.user.id).subscribe(x => (this.studyInquiries = x));
    this.api.getStudies().subscribe(all => {
      this.currentStudies = all.filter(s => s.status === 'currently_enrolling');
    });
    this.favoriteResources = this.user.user_favorites
      .filter(f => f.type === 'resource')
      .map(f => f.resource)
      .sort(a => a.id);
  }

  refreshParticipants() {
    if (this.user) {
      this.api.getUser(this.user.id).subscribe(u => {
        const newU = new User(u);
        this.self = newU.getSelf();
        this.dependents = newU.getDependents();
        if (newU.getSelf()) {
          this.api.getFlow(newU.getSelf().getFlowName(), newU.getSelf().id).subscribe(f => {
            this.selfPercentComplete = f.percentComplete();
            console.log('selfPercentComplete', this.selfPercentComplete);
          });
        }
      });
    }
  }

  getState() {
    if (!this.user) {
      // can happen if user logs out from this page.
      return ProfileState.NEEDS_USER;
    } else if (this.userMeta === undefined || this.forceMetaFormState) {
      return ProfileState.NEEDS_META;
    } else if (this.user.getSelf() === undefined) {
      return ProfileState.NEEDS_PARTICIPANT;
    } else {
      return ProfileState.HAS_PARTICIPANT;
    }
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.DEPENDENT]);
  }

  createMeta() {
    if (this.form.valid) {
      this.model.id = this.user.id;
      this.api.addUserMeta(this.model).subscribe(usermeta => {
        this.userMeta = usermeta;
        this.forceMetaFormState = false;
      });
    }
  }
}
