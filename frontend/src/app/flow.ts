export interface Flow {
  name: string;
  steps: Step[];
}

export interface Step {
  name: string;
  type: string;
  status: string;
  date_completed: Date;
}
