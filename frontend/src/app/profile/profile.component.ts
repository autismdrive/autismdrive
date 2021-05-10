import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { User } from '../_models/user';
import { ParticipantRelationship } from '../_models/participantRelationship';
import { Router } from '@angular/router';
import { Participant } from '../_models/participant';
import { Study } from '../_models/study';
import { StudyUser } from '../_models/study_user';
import { AuthenticationService } from '../_services/authentication/authentication-service';
import { Resource } from '../_models/resource';
import {AbstractControl, FormControl, FormGroup, ValidationErrors} from '@angular/forms';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {UserMeta} from '../_models/user_meta';

enum ProfileState {
  NO_PARTICIPANT = 'NO_PARTICIPANT',
  PARTICIPANT = 'PARTICIPANT'
}


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User;
  possibleStates = ProfileState;
  state = ProfileState.NO_PARTICIPANT;
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
  fields: FormlyFieldConfig[] = [{
    validators: {
      fieldMatch: {
        expression: (control) => {
          const {self_participant, guardian, professional, interested} = control.value;

          // at least one checkbox should be selected.
          if (!self_participant && !guardian && !professional && !interested) {
            return false;
          }
          return true;
        },
        message: 'Please select at least one option.'
      }
    },
    wrappers: ['group-validation'],
    fieldGroup: [
      {
        key: 'self_participant',
        type: 'checkbox',
        templateOptions: {label: 'I am autistic/I have autism', indeterminate: false},
      },
    {
      key: 'self_has_guardian',
      type: 'radio',
      templateOptions: {
        label: 'Do you have a legal guardian that helps you make day to day decisions?',
        options: [
          { value: true, label: 'Yes', id: '1' },
          { value: false, label: 'No', id: '2' },
        ]
      },
      expressionProperties: {
        'templateOptions.required': 'model.self_participant',
      },
      hideExpression: '!model.self_participant',
      },
      {
        key: 'guardian',
        type: 'checkbox',
        templateOptions: {label: 'I am the parent/legal guardian of someone with autism', indeterminate: false},
      },
      {
        key: 'guardian_has_dependent',
        type: 'radio',
        templateOptions: {
          label: 'Are you their legal guardian?',
          options: [
            {value: true, label: 'Yes', id: '3'},
            {value: false, label: 'No', id: '4'},
          ]
        },
        expressionProperties: {
          'templateOptions.required': 'model.guardian',
        },
        hideExpression: '!model.guardian',
      },
      {
        key: 'professional',
        type: 'checkbox',
        templateOptions: {label: 'I am a professional who works with the autism community', indeterminate: false},
      },
      {
        key: 'interested',
        type: 'checkbox',
        templateOptions: {label: 'None of the above, but I am interested in autism research and resources', indeterminate: false},
      },
    ]
  }];


  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router) {

    this.authenticationService.currentUser.subscribe(
      user => {
        this.user = user;
        console.log(user);
        this.self = user.getSelf();
        this.dependents = user.getDependents();
        this.state = this.getState();
        this.loading = false;
      }, error1 => {
        console.error(error1);
        this.user = null;
        this.loading = false;
      });
  }

  ngOnInit() {
    this.refreshParticipants();
    this.api.getUserStudyInquiries(this.user.id).subscribe( x => this.studyInquiries = x );
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
      this.api.getUser(this.user.id).subscribe( u => {
        const newU = new User(u);
        this.self = newU.getSelf();
        this.dependents = newU.getDependents();
        this.api.getFlow(newU.getSelf().getFlowName(), newU.getSelf().id).subscribe(
          f => {
            this.selfPercentComplete = f.percentComplete();
            console.log('selfPercentComplete', this.selfPercentComplete);
          }
        );
      });
    }
  }


  getState() {
    if (!this.user) {  // can happen if user logs out from this page.
      return null;
    } else if (this.user.getSelf() === undefined) {
      return ProfileState.NO_PARTICIPANT;
    } else {
      return ProfileState.PARTICIPANT;
    }
  }

  enrollSelf($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.SELF_PARTICIPANT]);
  }

  enrollGuardian($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.SELF_GUARDIAN]);
  }

  enrollDependent($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.DEPENDENT]);
  }

  enrollProfessional($event) {
    $event.preventDefault();
    this.router.navigate(['terms', ParticipantRelationship.SELF_PROFESSIONAL]);
  }

  enrollInterested($event) {
    $event.preventDefault();
    console.log(this.model);
    this.router.navigate(['meta']);
    // this.router.navigate(['terms', ParticipantRelationship.SELF_INTERESTED]);
  }

  // WIP - submit action
  enrollSubmit() {
    console.log('The Model is', this.model);
    if (this.form.valid) {
      // Need to reroute properly
      this.model.user_id = this.user.id;
      this.api.addUserMeta(this.model).subscribe( usermeta => {
          this.router.navigate(['meta']);
      });
    }
  }

}
