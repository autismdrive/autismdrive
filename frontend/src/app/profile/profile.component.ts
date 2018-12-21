import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';
import { FormArray, FormGroup } from '@angular/forms';
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
                type: 'phone',
                label: 'Preferred phone number',
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
      ],
    },
    {
      label: 'Address',
      description: '',
      fields: [
        {
          key: 'country',
          type: 'input',
          templateOptions: {
            label: 'Country',
            required: true,
          },
        },
      ],
    },
    {
      label: 'Day of the trip',
      description: '',
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
