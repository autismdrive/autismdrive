export interface EmailLog {
  id: number;
  user_id: number;
  type: string;
  tracking_code: string;
  viewed: boolean;
  date_viewed: string;
}
