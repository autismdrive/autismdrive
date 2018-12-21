import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';
import { FormArray, FormGroup, EmailValidator } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';

export interface StepType {
  label: string;
  description: string;
  fields: FormlyFieldConfig[];
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  session: User;
  activeStep = 0;

  model = {};
  steps: StepType[] = [
    {
      label: 'Research Registrant Contact Information',
      description: 'Please answer the following questions about YOURSELF (* indicates required response):',
      fields: [
        {
          key: 'firstname',
          type: 'input',
          templateOptions: {
            label: 'First name',
            required: true,
          },
        },
        {
          key: 'lastname',
          type: 'input',
          templateOptions: {
            label: 'Last name',
            required: true,
          },
        },
        {
          key: 'nickname',
          type: 'input',
          templateOptions: {
            label: 'Nickname',
            required: false,
          },
        },
        {
          key: 'phone',
          wrappers: ['card'],
          templateOptions: { label: 'Phone' },
          fieldGroup: [
            {
              key: 'phone',
              type: 'input',
              templateOptions: {
                required: true,
                type: 'tel',
                label: 'Preferred phone number (including area code)',
              },
              validators: {
                validation: ['phone'],
              },
            },
            {
              key: 'phoneType',
              type: 'radio',
              templateOptions: {
                label: '',
                placeholder: '',
                description: '',
                required: true,
                options: [
                  { value: 'home', label: 'Home' },
                  { value: 'cell', label: 'Cell' },
                ],
              },
            },
            {
              key: 'phoneType',
              type: 'radio',
              defaultValue: true,
              templateOptions: {
                label: 'Is it okay to leave a voicemail message at this number?',
                required: false,
                options: [
                  { value: true, label: 'Yes' },
                  { value: false, label: 'No' },
                ],
              },
            },
            {
              key: 'contactTimes',
              type: 'textarea',
              templateOptions: {
                label: `Some research studies might involve a phone call.
                        If that’s the case, when would be the best times of day to call you?`,
                required: false,
              },
            },
          ],
        },
        {
          key: 'email',
          type: 'input',
          templateOptions: {
            label: 'Email',
            type: 'email',
            required: true,
          },
          validators: {
            validation: ['email'],
          },
        },
        {
          key: 'address',
          wrappers: ['card'],
          templateOptions: { label: 'Address' },
          fieldGroup: [
            {
              key: 'streetAddress',
              type: 'input',
              templateOptions: {
                label: 'Street Address',
                required: true,
              },
            },
            {
              key: 'city',
              type: 'input',
              templateOptions: {
                label: 'Town/City',
                required: false,
              },
            },
            {
              key: 'state',
              type: 'input',
              templateOptions: {
                label: 'State',
                required: false,
              },
            },
            {
              key: 'zip',
              type: 'input',
              templateOptions: {
                type: 'number',
                label: 'Zip',
                max: 99999,
                min: 0,
                pattern: '\\d{5}',
                required: true,
              },
            },
          ],
        },
        {
          key: 'marketing',
          wrappers: ['card'],
          templateOptions: { label: 'How did you hear about us?' },
          fieldGroup: [
            {
              key: 'marketingChannel',
              type: 'radio',
              className: 'vertical-radio-group',
              templateOptions: {
                label: '',
                placeholder: '',
                description: '',
                required: true,
                options: [
                  { value: '1', label: 'Internet' },
                  { value: '2', label: 'Health care provider (doctor, speech therapist, etc)' },
                  { value: '3', label: 'Teacher or school' },
                  { value: '4', label: 'Word of mouth (friend, family member, etc)' },
                  { value: '5', label: 'Community event (autism walk, resource fair, etc.)' },
                  { value: '6', label: 'Television or radio (CNN, NPR, local news, etc.)' },
                  { value: '7', label: 'While participating in a research study' },
                  { value: '8', label: 'Other' },
                ],
              },
            },
            {
              key: 'marketingChannelOther',
              type: 'input',
              templateOptions: {
                placeholder: 'Where did you hear about us?'
              },
              hideExpression: '!(model.marketingChannel && (model.marketingChannel === "8"))',
            },
          ]
        },
      ],
    },
    {
      label: 'Respondent’s Demographics',
      description: 'Please answer the following questions about YOURSELF (* indicates required response):',
      fields: [
        {
          key: 'day',
          type: 'input',
          templateOptions: {
            type: 'date',
            label: 'Day of the trip',
            required: true,
          },
        },
      ],
    },
  ];

  form = new FormArray(this.steps.map(() => new FormGroup({})));
  options = this.steps.map(() => <FormlyFormOptions>{});

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.api.getSession().subscribe(user => {
      console.log(user);
      this.session = user;
    }, error1 => {
      this.session = null;
    });
  }

  prevStep(step: number) {
    this.activeStep = step - 1;
  }

  nextStep(step: number) {
    this.activeStep = step + 1;
  }

  submit() {
    alert(JSON.stringify(this.model));
  }
}
