export interface StepLog {
  id: number;
  questionnaire_name: string;
  questionnaire_id: number;
  flow: string;
  participant_id: number;
  user_id: number;
  date_completed: string;
  time_on_task_ms: number;
}
