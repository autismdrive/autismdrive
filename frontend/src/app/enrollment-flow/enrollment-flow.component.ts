import { Component, OnInit } from '@angular/core';
import { FormArray, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FormlyFormOptions } from '@ngx-formly/core';
import * as flatten from 'flat';
import { keysToCamel, toCamel } from 'src/util/snakeToCamel';
import { ApiService } from '../services/api/api.service';
import { QuestionnaireStep } from '../step';
import { User } from '../user';
import { Participant } from '../participant';
import { Flow } from '../flow';


@Component({
  selector: 'app-enrollment-flow',
  templateUrl: './enrollment-flow.component.html',
  styleUrls: ['./enrollment-flow.component.scss']
})
export class EnrollmentFlowComponent implements OnInit {
  user: User;
  participant: Participant;
  flow: Flow;

  stepName: string;
  activeStep = 0;
  loading = true;
  stepNames = [];
  flowName: string;
  participantId: number;

  model: any = {};
  step: QuestionnaireStep;
  form: FormArray;
  options: FormlyFormOptions;

  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.api.getSession().subscribe(userProps => {
      this.user = new User(userProps);
      this.route.params.subscribe(params => {
        this.stepName = params.stepName || '';
        this.flowName = params.flowName || '';

        if (params.hasOwnProperty('participantId')) {
          console.log(`Called with a participant id of ${params.participantId}`);
          console.log('User Participants: ', this.user.participants);
          this.participantId = parseInt(params.participantId, 10);

          for (const up of this.user.participants) {
            if (up.id === this.participantId) {
              this.participant = up;
            }
          }
        } else {
          this.participantId = undefined;
        }

        if (isFinite(this.participantId) && (this.flowName !== '')) {
          console.log('this.flowName', this.flowName);

          this.api
            .getFlow(this.flowName, this.participantId)
            .subscribe(f => {
              this.flow = f;
              this.stepNames = f.steps.map(s => s.name);

              if (this.stepName === '') {
                this.stepName = this.stepNames[0];
              }

              this.api.getQuestionnaireMeta(this.flowName, this.stepName).subscribe(q => {
                this.step = this._infoToFormlyForm(q.get_meta, this.stepName);
                console.log('This is still loading? ' + this.loading);
                console.log('The Step is set to ', this.step);
                this.form = new FormArray([new FormGroup({})]);
                this.options = {
                  formState: {
                    mainModel: this.model
                  }
                };

                this.model.preferred_name = this.participant.name;
                this.model.is_self = this.user.isSelf(this.participant);
                this.loading = false;
              });
            });
        }
      });
    });
  }

  ngOnInit() {
  }


  private _infoToFormlyForm(info, stepName, fieldsType = 'fields'): QuestionnaireStep {
    const step = new QuestionnaireStep({
      id: info.id,
      name: stepName,
      label: '',
      description: '',
      fields: [],
      fieldGroup: [],
    });
    const stepFields = [];

    //  First, Process the table object.
    const table = info['table'];
    Object.keys(table).forEach(tableKey => {
      step[toCamel(tableKey)] = table[tableKey];
    });

    // Next process the Field Groups
    if ('field_groups' in info) {
      const field_groups = info['field_groups'];
      Object.keys(field_groups).forEach(wrapperKey => {
        // Clone the wrapper object so we can delete the original later
        const wrapper = this.clone(field_groups[wrapperKey]);
        const fgFields = field_groups[wrapperKey].fields || [];
        wrapper.key = wrapperKey;

        if (wrapper.type === 'repeat') {
          // Recursively process sub-forms and insert them into fieldArray.
          // Fields will be inserted into 'fieldGroup', rather than 'fields' attribute.
          wrapper.fieldArray = this._infoToFormlyForm(info[wrapperKey], wrapperKey, 'fieldGroup');
        } else {
          wrapper.fieldGroup = this._mapFieldnamesToFieldGroup(fgFields, info);

          // Remove the fields array from the wrapper object,
          // since all its child fields are now inside the
          // fieldGroup attribute
          delete wrapper.fields;
        }
        stepFields.push(keysToCamel(wrapper));
      });
    }

    //  Handle the remaining fields.
    Object.keys(info).forEach(key => {
      const item = info[key];
      if (item && key !== 'table' && key !== 'field_groups') {
        item.key = key;
        item.name = key;
        stepFields.push(keysToCamel(item));
        console.log('Also adding these fields, where key is : ' + key, this.clone(item));
      }
    });

    stepFields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    stepFields.forEach(f => step[fieldsType].push(f));
    console.log(step);
    return step;
  }

  prevStep(step: number) {
    this.activeStep = step - 1;
    this.submit();
  }

  nextStep(step: number) {
    this.activeStep = step + 1;
    this.submit();
  }

  setActiveStep(step: number) {
    this.activeStep = step;
    this.submit();
  }

  submit() {
    // Flatten the model
    const flattened = flatten(this.model, { safe: true });

    // Rename the keys
    const options = {
      participant_id: this.participantId
    };
    const pattern = /^(.*)\./gi;
    Object.keys(flattened).map(oldKey => {
      const newKey = oldKey.replace(pattern, '');
      options[newKey] = flattened[oldKey];
    });

    if (isFinite(this.step.id)) {
      this.api.updateQuestionnaire(this.step.name, this.step.id, options).subscribe(response => {
        // !!! TO DO - Update form with saved values
        this.router.navigate(['participant', this.participantId, this.flowName, this.stepNames[this.activeStep]]);
      });
    } else {
      this.api.submitQuestionnaire(this.flowName, this.step.name, options).subscribe(response => {
        // !!! TO DO - Update form with saved values
        this.router.navigate(['participant', this.participantId, this.flowName, this.stepNames[this.activeStep]]);
      });
    }
  }

  clone(o: any): any {
    return JSON.parse(JSON.stringify(o));
  }

  private _mapFieldnamesToFieldGroup(fieldnames: string[], parentObject) {
    return fieldnames.map((childKey: string) => {
      const childField = this.clone(parentObject[childKey]);
      childField.key = childKey;
      childField.name = childKey;

      // Remove the field from the 'all' object, since we've
      // now copied it to its parent fieldGroup
      delete parentObject[childKey];
      return keysToCamel(childField);
    });
  }

}
