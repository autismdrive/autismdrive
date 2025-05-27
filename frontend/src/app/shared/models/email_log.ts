export interface EmailLog {
  id: number;
  user_id: number;
  type: 'reset_email' | 'study_inquiry_email' | 'confirm_email';
  tracking_code: string;
  viewed: boolean;
  date_viewed: string;
}
