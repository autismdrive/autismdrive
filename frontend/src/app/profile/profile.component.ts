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
import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';

enum ProfileState {
  NO_PARTICIPANT = 'NO_PARTICIPANT',
  PARTICIPANT = 'PARTICIPANT'
}

export interface Task {
  name: string;
  completed: boolean;
  subtasks?: Task[];
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
  radioData: String;
  model: any = {};
  form: FormGroup;
  options: FormlyFormOptions;
  fields: FormlyFieldConfig[] = [
    {
      key: 'self',
      type: 'checkbox',
      templateOptions: {
        label: 'I am an autistic adult or adult with autism.',
        indeterminate: false,
        required: false,
      },
      validation: {
        show: true,
      },
      expressionProperties: {
        'templateOptions.required' : 'model.checked',
      },
    },
    {
      key: 'selfRadio',
      type: 'radio',
      templateOptions: {
        label: 'Do you have a legal guardian?',
        name: 'self-sel',
        options: [{ value: 'Yes', key: 'Other'}, { value: 'No', key: 'Self'}],
        change: () => this.radioData = this.model.selfRadio,
      },
      hideExpression: '!model.self',
    },
    {
      key: 'guardian',
      type: 'checkbox',
      templateOptions: {
        label: 'I am the parent of someone with autism.',
        indeterminate: false,
        required: false,
      }
    },
    {
      key: 'guardianRadio',
      type: 'radio',
      templateOptions: {
        label: 'Are you their legal guardian?',
        name: 'guardian-sel',
        options: [{ value: 'Yes', key: 'Guardian' }, { value: 'No', key: 'Other' }],
        change: () => this.radioData = this.model.guardianRadio,
      },
      hideExpression: '!model.guardian',
    },
    {
      key: 'professional',
      name: 'Professional',
      type: 'checkbox',
      templateOptions: {
        label: 'I am a professional who works with the autism community.',
        change: () => console.log(this.model),
        indeterminate: false,
        required: false,
      }
    },
    {
      key: 'other',
      type: 'checkbox',
      templateOptions: {
        label: 'None of the above, but I am interested in autism research and resources.',
        indeterminate: false,
        required: false,
        }
      }
    ];

  constructor(private authenticationService: AuthenticationService,
              private api: ApiService,
              private router: Router) {

    this.authenticationService.currentUser.subscribe(
      user => {
        this.user = user;
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
    this.radioData = 'Other';
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

  enrollSelf() {
    this.router.navigate(['terms', ParticipantRelationship.SELF_PARTICIPANT]);
  }

  enrollGuardian() {
    this.router.navigate(['terms', ParticipantRelationship.SELF_GUARDIAN]);
  }

  enrollDependent() {
    this.router.navigate(['terms', ParticipantRelationship.DEPENDENT]);
  }

  enrollProfessional() {
    this.router.navigate(['terms', ParticipantRelationship.SELF_PROFESSIONAL]);
  }

  submitEnroll() {
    if (this.radioData === 'Self') {
      console.log(this.radioData);
      this.enrollSelf();
    }
    if (this.radioData === 'Guardian') {
      console.log(this.radioData);
      this.enrollGuardian();
    }
    if (this.radioData === 'Dependent') {
      this.enrollDependent();
    }
    if (this.radioData === 'Professional') {
      this.enrollProfessional();
    }
    if (['Other', 'SelfIneligible', 'ParentIneligible'].indexOf(this.radioData.toString()) > -1) {
      console.log(this.radioData);
      this.enrollSelf(); // delete this
    }
  }

  submitEnroll2() {
    switch (this.radioData) {
      case 'Self':
        this.enrollSelf();
        break;
      case 'Guardian':
        this.enrollGuardian();
        break;
      case 'Dependent':
        this.enrollDependent();
        break;
      case 'Professional':
        this.enrollProfessional();
        break;
      default: // Add Default page
        break;
      }
  }
}
