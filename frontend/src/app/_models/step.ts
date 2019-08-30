
export interface Step {
  name: string;
  type: string;
  description: string;
  label: string;
  status: string;
  date_completed: Date;
  questionnaire_id?: number;
}

export class StepStatus {
  public static readonly COMPLETE = 'COMPLETE';
  public static readonly INCOMPLETE = 'INCOMPLETE';
}

