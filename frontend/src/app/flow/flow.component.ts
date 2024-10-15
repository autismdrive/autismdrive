import {MediaMatcher} from '@angular/cdk/layout';
import {ChangeDetectorRef, Component, OnDestroy, ViewChild} from '@angular/core';
import {AbstractControl, FormGroup} from '@angular/forms';
import {MatDrawer} from '@angular/material/sidenav';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {scrollToFirstInvalidField, scrollToTop} from '@util/scrollToTop';
import {keysToCamel} from '@util/snakeToCamel';
import {DeviceDetectorService} from 'ngx-device-detector';
import {Flow} from '@models/flow';
import {Participant} from '@models/participant';
import {Step, StepStatus} from '@models/step';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {GoogleAnalyticsService} from '@services/google-analytics/google-analytics.service';

enum FlowState {
  INTRO = 'intro',
  LOADING = 'loading',
  COMPLETE = 'complete',
  SHOW_FORM = 'form',
}

@Component({
  selector: 'app-flow',
  templateUrl: './flow.component.html',
  styleUrls: ['./flow.component.scss'],
})
export class FlowComponent implements OnDestroy {
  mobileQuery: MediaQueryList;
  user: User;
  participant: Participant;
  flow: Flow;
  activeStep = 0;
  flowState = FlowState;
  state = FlowState.LOADING;
  startTime: number;
  showResubmitMessage = false;
  hideForm = false;
  sidebarOpen = true;
  model: any = {};
  form: FormGroup;
  fields = [];
  options: FormlyFormOptions;
  sidenavElement: MatDrawer;
  private _mobileQueryListener: () => void;

  constructor(
    media: MediaMatcher,
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private changeDetectorRef: ChangeDetectorRef,
    private deviceDetectorService: DeviceDetectorService,
    private googleAnalyticsService: GoogleAnalyticsService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    // We will change the display slightly based on mobile vs desktop
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    // Using addEventListener causes page failures for older Safari / webkit / iPhone
    // this.mobileQuery.addEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.addListener(this._mobileQueryListener);
    this._mobileQueryListener = () => this._updateSidenavState();
    window.addEventListener('resize', this._mobileQueryListener);

    this.authenticationService.currentUser.subscribe(user => {
      this.user = user;
      this.route.params.subscribe(params => {
        this.participant = this.user.getParticipantById(parseInt(params.participantId, 10));
        this.loadFlow(params.flowName);
      });
    });
  }

  @ViewChild(MatDrawer)
  set sidenav(value: MatDrawer) {
    this.sidenavElement = value;
    this._updateSidenavState();
  }

  ngOnDestroy(): void {
    // removeEventListener fails on older versions of iOS / Safari / iPhone
    // this.mobileQuery.removeEventListener('change', this._mobileQueryListener);
    // tslint:disable-next-line:deprecation
    this.mobileQuery.removeListener(this._mobileQueryListener);
    window.removeEventListener('resize', this._mobileQueryListener);
  }

  loadFlow(flowName: string) {
    this.api.getFlow(flowName, this.participant.id).subscribe(f => {
      this.flow = new Flow(f);
      if (this.flow.percentComplete() === 0) {
        this.state = this.flowState.INTRO;
      } else {
        this.goToNextAvailableStep();
      }
      scrollToTop(this.deviceDetectorService);
    });
  }

  updateParticipant(participantId: number) {
    this.api.getParticipant(participantId).subscribe(p => {
      this.participant = p;
    });
  }

  goToNextAvailableStep() {
    // get the participant back first to catch any changes to the preferred name
    this.updateParticipant(this.participant.id);

    // Go to the next incomplete step.  Loop back around to the beginning of steps, in case an
    // earlier step is incomplete.  NOTE:  You will stay on the current step if it is not complete.

    if (this.flow.percentComplete() < 100) {
      let index = this.activeStep;
      if (this.flow.steps[this.activeStep].status === StepStatus.COMPLETE) {
        index++;
        while (index !== this.activeStep) {
          if (this.flow.steps[index] && this.flow.steps[index].status !== StepStatus.COMPLETE) {
            this.activeStep = index;
            break;
          }
          if (index >= this.flow.steps.length - 1) {
            index = 0;
          } else {
            index++;
          }
        }
      }
      this.loadActiveStep();
    } else {
      this.state = FlowState.COMPLETE;
      this.googleAnalyticsService.flowCompleteEvent(this.flow.name);
      scrollToTop(this.deviceDetectorService);
    }
  }

  goToStep(step: Step) {
    // get the participant back first to catch any changes to the preferred name
    this.updateParticipant(this.participant.id);

    for (let i = 0; i < this.flow.steps.length; i++) {
      if (this.flow.steps[i].name === step.name) {
        this.activeStep = i;
        break;
      }
    }
    this.loadActiveStep();
    if (this.mobileQuery.matches) {
      this.sidebarOpen = false;
    }
    scrollToTop(this.deviceDetectorService);
  }

  currentStep(): Step {
    return this.flow.steps[this.activeStep];
  }

  loadActiveStep() {
    const step = this.flow.steps[this.activeStep];
    this.api.getQuestionnaireMeta(this.flow.name, step.name).subscribe(q => {
      this.showResubmitMessage = false;
      this.hideForm = false;
      // Load the form with previously-submitted data, if available
      if (step.type === 'sensitive' && step.questionnaire_id > 0) {
        this.showResubmitMessage = true;
        this.hideForm = true;
        this.renderForm(step, q);
      } else if (step.questionnaire_id > 0) {
        this.api.getQuestionnaire(step.name, step.questionnaire_id).subscribe(qData => {
          this.model = qData;
          this.renderForm(step, q);
        });
      } else {
        this.renderForm(step, q);
      }
      scrollToTop(this.deviceDetectorService);
    });
    scrollToTop(this.deviceDetectorService);
  }

  highlightRequiredFields() {
    for (const fieldName of Object.keys(this.form.controls)) {
      const field: AbstractControl = this.form.controls[fieldName];
      field.updateValueAndValidity();
      field.markAsDirty();
    }

    scrollToFirstInvalidField(this.deviceDetectorService);
  }

  submit() {
    // force the correct participant id.
    this.model['participant_id'] = this.participant.id;
    this.model['time_on_task_ms'] = performance.now() - this.startTime;

    // Post to the questionnaire endpoint, and then reload the flow.
    if (this.currentStep().questionnaire_id > 0 && this.currentStep().type !== 'sensitive') {
      this.api
        .updateQuestionnaire(this.currentStep().name, this.currentStep().questionnaire_id, this.model)
        .subscribe(() => {
          this.googleAnalyticsService.stepCompleteEvent(this.currentStep().name);
          this.loadFlow(this.flow.name);
          scrollToTop(this.deviceDetectorService);
        });
    } else {
      this.api.submitQuestionnaire(this.flow.name, this.currentStep().name, this.model).subscribe(() => {
        this.googleAnalyticsService.stepCompleteEvent(this.currentStep().name);
        this.loadFlow(this.flow.name);
        scrollToTop(this.deviceDetectorService);
      });
    }
  }

  numCompletedSteps() {
    return this.flow.steps.filter(s => s.status === StepStatus.COMPLETE).length;
  }

  numTotalSteps() {
    return this.flow.steps.length;
  }

  toggleSidenav() {
    this.sidebarOpen = !this.sidebarOpen;
    this.sidenavElement.toggle(this.sidebarOpen, 'mouse').then(() => {
      scrollToTop(this.deviceDetectorService);
    });
  }

  private renderForm(step: Step, q_meta) {
    this.startTime = performance.now();
    this.fields = this.infoToForm(q_meta);
    this.form = new FormGroup({});
    this.options = {
      formState: {
        mainModel: this.model,
        preferredName: this.participant.name,
      },
    };
    this.state = this.flowState.SHOW_FORM;
    scrollToTop(this.deviceDetectorService);
  }

  private infoToForm(info: any): FormlyFieldConfig[] {
    const fields = [];
    for (const field of info.fields) {
      if (field.fieldArray) {
        // noinspection JSConstantReassignment
        field.fieldArray.model = this.model[field.name];
      }
      fields.push(keysToCamel(field));
    }
    fields.sort((f1, f2) => f1.displayOrder - f2.displayOrder);
    return fields;
  }

  private _updateSidenavState() {
    if (this.sidenavElement) {
      if (this.mobileQuery.matches) {
        this.sidenavElement.close();
        this.sidebarOpen = false;
      } else {
        this.sidenavElement.open();
        this.sidenavElement.disableClose = true;
        this.sidebarOpen = true;
      }
    }

    this.changeDetectorRef.detectChanges();
  }
}
