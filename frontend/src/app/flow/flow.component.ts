import { Component, OnInit } from '@angular/core';
import {Form, FormArray, FormGroup} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import {FieldArrayType, FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import { keysToCamel} from 'src/util/snakeToCamel';
import { ApiService } from '../services/api/api.service';
import { User } from '../user';
import { Participant } from '../participant';
import {Flow} from '../flow';
import {Step, StepStatus} from '../step';


@Component({
  selector: 'app-flow',
  templateUrl: './flow.component.html',
  styleUrls: ['./flow.component.scss']
})
export class FlowComponent implements OnInit {

  user: User;
  participant: Participant;
  flow: Flow;

  activeStep = 0;
  loading = true;

  model: any = {};
  form: FormArray;
  fields: FormlyFieldConfig;
  options: FormlyFormOptions;

  static clone(o: any): any {
    return JSON.parse(JSON.stringify(o));
  }

  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.api.getSession().subscribe(userProps => {
      this.user = new User(userProps);
      console.log('User Loaded:' + this.user.id);
      this.route.params.subscribe(params => {
        this.participant = this.user.getParticipantById(parseInt(params.participantId, 10));
        console.log('Participant loaded:' + this.participant.id);
        this.loadFlow(params.flowName);
      });
    });
  }

  ngOnInit() {
  }

  loadFlow(flowName: string) {
    this.api
      .getFlow(flowName, this.participant.id)
      .subscribe(f => {
        this.flow = new Flow(f);
        console.log('Flow Loaded:' + this.flow.name);
        this.goToNextAvailableStep();
      });
  }

  goToNextAvailableStep() {
    // Go to the next incomplete step.  Loop back around to the beginning of steps, in case an
    // earlier step is incomplete.  NOTE:  You will stay on the current step if it is not complete.
    console.log('The flow is ' + this.flow.percentComplete() + '% complete.');
    if (this.flow.percentComplete() < 100) {
      let index = this.activeStep;
      if (this.flow.steps[this.activeStep].status === StepStatus.COMPLETE) {
        console.log('Processing index :' + index);
        index++;
        while (index !== this.activeStep) {
          if (this.flow.steps[index].status !== StepStatus.COMPLETE) {
            this.activeStep = index;
            break;
          }
          if (index >= this.flow.steps.length - 1) { index = 0; } else { index++; }
        }
      }
      console.log('The Active Step index is :' + this.activeStep);
      this.loadActiveStep();
    } else {
      console.log('This flow is already completed.');
    }
  }

  goToStep(step: Step) {
    console.log('Requested to set the step to ' + step.name);
    for (let i = 0; i < this.flow.steps.length; i++) {
      if (this.flow.steps[i].name === step.name) {
        console.log('Setting Active Step to ' + i);
        this.activeStep = i;
        break;
      }
    }
    this.loadActiveStep();
  }

  currentStep(): Step {
    return this.flow.steps[this.activeStep];
  }

  loadActiveStep() {
    const step = this.flow.steps[this.activeStep];
    this.api.getQuestionnaireMeta(this.flow.name, step.name).subscribe(q => {
      // Load the form with previously-submitted data, if available
      if (step.questionnaire_id > 0) {
        this.api
          .getQuestionnaire(step.name, step.questionnaire_id)
          .subscribe(qData => {
            this.model = qData;
            this.renderForm(step, q);
          });
      } else {
        this.renderForm(step, q);
      }
    });
  }


  private renderForm(step: Step, q_meta) {
    this.fields = {};
    this.fields = this.infoToForm(q_meta);
    console.log('Model: ', this.model);
    console.log('Fields: ', this.fields);
    console.log('Step:', step);

    this.form = new FormArray([new FormGroup({})]);
    this.options = {
      formState: {
        mainModel: this.model
      }
    };

    this.model.preferred_name = this.participant.name;
    this.model.is_self = this.user.isSelf(this.participant);
    this.loading = false;
  }

  private infoToForm(info) {
    const fields = []
    for (const field of info.fields) {
      if (field.fieldArray) {
        field.fieldArray.model = this.model[field.name];
      }
      fields.push(keysToCamel(field));

    }
    fields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    return fields;
  }

  private _infoToFormlyForm(info, fieldsType = 'fields'): FormlyFieldConfig {

    console.log("info", info);
    return info.fields;
    const stepFields = [];
    const formlyFields = {};

    // Next process the Field Groups
    if ('field_groups' in info) {
      const field_groups = info['field_groups'];
      Object.keys(field_groups).forEach(wrapperKey => {
        // Clone the wrapper object so we can delete the original later
        const wrapper = FlowComponent.clone(field_groups[wrapperKey]);
        const fgFields = field_groups[wrapperKey].fields || [];

        if (wrapper.type === 'repeat') {

          wrapper.fieldArray = fgFields;


        } else {
          wrapper.fieldGroup = fgFields; // this._mapFieldnamesToFieldGroup(fgFields, info);
          wrapper.fieldGroup.model = this.model;
          console.log('FieldGroup: ', wrapper.fieldGroup);
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
      }
    });

    stepFields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    formlyFields[fieldsType] = [];
    stepFields.forEach(f => formlyFields[fieldsType].push(f));
    // console.log('The Fields Are ', formlyFields);
    return formlyFields;
  }

  submit() {
    // force the correct participant id.
    this.model['participant_id'] = this.participant.id;

    // Post to the questionnaire endpoint, and then reload the flow.
    if (this.currentStep().questionnaire_id > 0) {
      this.api.updateQuestionnaire(this.currentStep().name, this.currentStep().questionnaire_id, this.model)
        .subscribe(() => {
        this.loadFlow(this.flow.name);
      });
    } else {
      this.api.submitQuestionnaire(this.flow.name, this.currentStep().name, this.model)
        .subscribe(() => {
          this.loadFlow(this.flow.name);
      });
    }
  }

}
