export enum StepType {
  SENSITIVE = 'sensitive',
  IDENTIFYING = 'identifying',
  UNRESTRICTED = 'unrestricted',
  SUB_TABLE = 'sub-table',
}

export enum StepStatus {
  COMPLETE = 'COMPLETE',
  INCOMPLETE = 'INCOMPLETE',
}

export interface Step {
  name: string;
  type: StepType;
  description: string;
  label: string;
  status: StepStatus;
  date_completed: Date;
  questionnaire_id?: number;
}
