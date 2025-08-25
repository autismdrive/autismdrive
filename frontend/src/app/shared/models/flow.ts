import {Step} from './step';

export enum FlowName {
  SELF_INTAKE = 'self_intake',
  DEPENDENT_INTAKE = 'dependent_intake',
  GUARDIAN_INTAKE = 'guardian_intake',
  PROFESSIONAL_INTAKE = 'professional_intake',
  INTERESTED_INTAKE = 'interested_intake',
  REGISTRATION = 'registration',
  SKILLSTAR = 'skillstar',
}

export class Flow {
  name: FlowName;
  steps: Step[];

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }

  isComplete(): boolean {
    return this.percentComplete() === 1;
  }

  percentComplete(): number {
    if (this.steps && this.steps.length > 0) {
      const completeSteps = this.steps.filter(s => s.status === 'COMPLETE');
      return (completeSteps.length / this.steps.length) * 100;
    } else {
      return 0;
    }
  }
}
