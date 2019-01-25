import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';
import { FormArray, FormGroup, EmailValidator } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { QuestionnaireStep } from '../step';
import * as flatten from 'flat';
import { keysToCamel, toCamel } from 'src/util/snakeToCamel';


export interface StarProfileModel {
  enrollingFor?: string;
  dependentFirstName?: string;
  dependentLastName?: string;
  dependentNickname?: string;
  firstname?: string;
  lastname?: string;
  nickname?: string;
  phone?: string;
  phoneType?: string;
  contactTimes?: string;
  email?: string;
  address?: string;
  streetAddress?: string;
  city?: string;
  state?: string;
  zip?: string;
  marketing?: string;
  marketingChannel?: string;
  marketingChannelOther?: string;
  birthdate?: string;
  sex?: string;
  race?: string;
  raceBlack?: string;
  raceAsian?: string;
  raceWhite?: string;
  raceHispanic?: string;
  raceNative?: string;
  racePacific?: string;
  raceOther?: string;
  raceOtherValue?: string;
  primaryLanguageIsEnglish?: string;
  relationshipToDependent?: string;
  relationshipToDependentOtherValue?: string;
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  session: User;
  activeStep = 0;
  loading = true;

  model: StarProfileModel = {};
  steps: QuestionnaireStep[] = [];

  formlySteps = [
    {
      label: 'UVA Research Registry Enrollment',
      description: '',
      fields: [
        {
          key: 'enrollingFor',
          type: 'radio',
          defaultValue: 'self',
          modelOptions: {
            updateOn: 'change',
          },
          templateOptions: {
            label: 'Are you enrolling yourself or someone else?',
            required: true,
            options: [
              { value: 'self', label: 'Myself' },
              { value: 'dependent', label: 'My child or a person I have legal guardianship over*' },
            ],
            description: '*You must be this person’s legal guardian in order to enroll them.'
          },
        },
      ]
    },
    {
      label: 'Dependent Information',
      description: `Please answer the following questions about your child
        or the person with autism on whom you are providing information:`,
      fields: [
        {
          key: 'dependentFirstName',
          type: 'input',
          templateOptions: {
            label: 'First name',
            required: true,
          },
        },
        {
          key: 'dependentLastName',
          type: 'input',
          templateOptions: {
            label: 'Last name',
            required: true,
          },
        },
        {
          key: 'dependentNickname',
          type: 'input',
          templateOptions: {
            label: 'Nickname',
            required: false,
          },
        },
      ]

    },
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
              key: 'canLeaveVoicemail',
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
          key: 'birthdate',
          type: 'datepicker',
          templateOptions: {
            label: 'Your date of birth',
            required: true,
          },
        },
        {
          key: 'sex',
          type: 'radio',
          templateOptions: {
            label: 'Your biological sex',
            placeholder: '',
            description: '',
            required: false,
            options: [
              { value: 'male', label: 'Male' },
              { value: 'female', label: 'Female' },
              { value: 'other', label: 'Other' },
              { value: 'no_answer', label: 'Prefer not to answer' },
            ],
          },
        },
        {
          key: 'race',
          type: 'multicheckbox',
          className: 'vertical-radio-group',
          templateOptions: {
            options: [
              {
                key: 'raceBlack',
                value: 'Black / African / African American'
              },
              {
                key: 'raceAsian',
                value: 'Asian / Asian American'
              },
              {
                key: 'raceWhite',
                value: 'White / Caucasian'
              },
              {
                key: 'raceHispanic',
                value: 'Hispanic / Latin(o / a)'
              },
              {
                key: 'raceNative',
                value: 'Native American / Alaska Native'
              },
              {
                key: 'racePacific',
                value: 'Pacific Islander'
              },
              {
                key: 'raceOther',
                value: 'Other'
              },
            ],
            label: 'Your race/ethnicity (select all that apply):'
          }
        },
        {
          key: 'raceOtherValue',
          type: 'input',
          templateOptions: {
            placeholder: 'Enter race/ethnicity'
          },
          hideExpression: '!model.raceOther',
        },
        {
          key: 'primaryLanguageIsEnglish',
          type: 'radio',
          defaultValue: true,
          templateOptions: {
            label: 'Is your primary language English?',
            required: false,
            options: [
              { value: true, label: 'Yes' },
              { value: false, label: 'No' },
            ],
          },
        },
        {
          key: 'relationshipToDependent',
          type: 'select',
          defaultValue: true,
          templateOptions: {
            label: 'Your relationship to dependent',
            required: false,
            options: [
              { value: '1', label: 'Biological mother' },
              { value: '2', label: 'Biological father' },
              { value: '3', label: 'Adoptive mother' },
              { value: '4', label: 'Adoptive father' },
              { value: '5', label: 'Other' },
            ],
          },
          hideExpression: '!((model.enrollingFor === "dependent") && model.dependentFirstName && model.dependentLastName)',
          expressionProperties: {
            'templateOptions.label': '"Your relationship to " + model.dependentFirstName + " " + model.dependentLastName'
          }
        },
        {
          key: 'relationshipToDependentOtherValue',
          type: 'input',
          templateOptions: {
            placeholder: 'Enter relationship'
          },
          hideExpression: '!(' +
            'model.enrollingFor === "dependent" && ' +
            'model.relationshipToDependent && ' +
            '(model.relationshipToDependent === "5")' +
            ')',
        },
      ]
    },


  ];

  form: FormArray;
  options;

  constructor(
    private api: ApiService
  ) {
    const stepKeys = ['contact', 'demographics'];
    let numStepsMapped = 0;

    // loop thru steps
    stepKeys.forEach(k => {
      this.api.getQuestionnaireMeta(k).subscribe(q => {
        this.steps.push(this.infoToFormlyForm(q.get_meta, k));

        numStepsMapped++;

        if (numStepsMapped === stepKeys.length) {
          this.form = new FormArray(this.steps.map(() => new FormGroup({})));
          this.options = this.steps.map(() => <FormlyFormOptions>{});
          this.loading = false;
        }
      });
    });
  }

  ngOnInit() {
    this.api.getSession().subscribe(user => {
      this.session = user;
    }, error1 => {
      this.session = null;
    });
  }

  infoToFormlyForm(info, questionnaireKey): QuestionnaireStep {
    const step = new QuestionnaireStep({
      id: info.id,
      key: questionnaireKey,
      label: '',
      description: '',
      fields: []
    });
    const stepFields = [];

    Object.keys(info).forEach(key => {
      const item = info[key];

      if (key === 'table') {
        Object.keys(item).forEach(tableKey => {
          step[toCamel(tableKey)] = item[tableKey];
        });
      } else if (key === 'field_groups') {
        Object.keys(item).forEach(wrapperKey => {

          // Clone the wrapper object so we can delete the original later
          const wrapper = JSON.parse(JSON.stringify(item[wrapperKey]));
          const fgFields = item[wrapperKey].fields || [];
          wrapper.key = wrapperKey;
          wrapper.fieldGroup = fgFields.map((childKey: string) => {
            const childField = JSON.parse(JSON.stringify(info[childKey]));
            childField.key = childKey;
            childField.name = childKey;

            // Remove the field from the 'all' object, since we've
            // now copied it to its parent fieldGroup
            delete info[childKey];
            return keysToCamel(childField);
          });

          // Remove the fields array from the wrapper object,
          // since all its child fields are now inside the
          // fieldGroup attribute
          delete wrapper.fields;
          stepFields.push(keysToCamel(wrapper));
        });
      } else if (item) {
        item.key = key;
        item.name = key;
        stepFields.push(keysToCamel(item));
      }
    });

    stepFields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    stepFields.forEach(f => step.fields.push(f));
    return step;
  }

  prevStep(step: number) {
    this.activeStep = step - 1;
  }

  nextStep(step: number) {
    this.activeStep = step + 1;
  }

  submit() {
    // Flatten the model
    const flattened = flatten(this.model, { safe: true });

    // Rename the keys
    const options = {};
    const pattern = /^(.*)\./gi;
    Object.keys(flattened).map(oldKey => {
      const newKey = oldKey.replace(pattern, '');
      options[newKey] = flattened[oldKey];
    });

    // Get the current step
    const step = this.steps[this.activeStep];

    if (isFinite(step.id)) {
      this.api.updateQuestionnaire(step.key, step.id, options).subscribe(response => {
        // Update form with saved values
      });
    } else {
      this.api.submitQuestionnaire(step.key, options).subscribe(response => {
        // Update form with saved values
      });
    }
  }

}
