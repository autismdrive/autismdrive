import { Component, OnInit } from '@angular/core';
import { FormArray, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FormlyFormOptions } from '@ngx-formly/core';
import * as flatten from 'flat';
import { keysToCamel, toCamel } from 'src/util/snakeToCamel';
import { ApiService } from '../api.service';
import { QuestionnaireStep } from '../step';
import { User } from '../user';


@Component({
  selector: 'app-enrollment-flow',
  templateUrl: './enrollment-flow.component.html',
  styleUrls: ['./enrollment-flow.component.scss']
})
export class EnrollmentFlowComponent implements OnInit {
  user: User;
  stepName: string;
  activeStep = 0;
  loading = true;
  stepNames = [
    'identification',
    'contact',
    'demographics',
    'home',
    'evaluation_history'
  ];

  model = {};
  step: QuestionnaireStep;
  form: FormArray;
  options;

  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.api.getSession().subscribe(user => {
      this.user = user;
      this.route.params.subscribe(params => {
        const stepName = params.stepName || '';

        if (stepName !== '') {
          this.api.getQuestionnaireMeta(stepName).subscribe(q => {
            this.step = this._infoToFormlyForm(q.get_meta, stepName);
            this.form = new FormArray([new FormGroup({})]);
            this.options = <FormlyFormOptions>{};
            this.loading = false;
          });

        } else {
          this.loading = false;
        }
      });
    }, error1 => {
      this.user = null;
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

    Object.keys(info).forEach(key => {
      const item = info[key];

      if (key === 'table') {
        Object.keys(item).forEach(tableKey => {
          step[toCamel(tableKey)] = item[tableKey];
        });
      } else if (key === 'field_groups') {
        Object.keys(item).forEach(wrapperKey => {

          // Clone the wrapper object so we can delete the original later
          const wrapper = this.clone(item[wrapperKey]);
          const fgFields = item[wrapperKey].fields || [];
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
      } else if (item) {
        item.key = key;
        item.name = key;
        stepFields.push(keysToCamel(item));
      }
    });

    stepFields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    stepFields.forEach(f => step[fieldsType].push(f));
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
    const options = {};
    const pattern = /^(.*)\./gi;
    Object.keys(flattened).map(oldKey => {
      const newKey = oldKey.replace(pattern, '');
      options[newKey] = flattened[oldKey];
    });

    if (isFinite(this.step.id)) {
      this.api.updateQuestionnaire(this.step.name, this.step.id, options).subscribe(response => {
        // Update form with saved values
        this.router.navigate(['profile', 'enrollment', this.stepNames[this.activeStep]]);
      });
    } else {
      this.api.submitQuestionnaire(this.step.name, options).subscribe(response => {
        // Update form with saved values
        this.router.navigate(['profile', 'enrollment', this.stepNames[this.activeStep]]);
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
