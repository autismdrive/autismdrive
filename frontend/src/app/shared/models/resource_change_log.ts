export interface ResourceChangeLog {
  id: number;
  type: string;
  user_id: number;
  user_email: string;
  resource_id: number;
  resource_title: string;
  last_updated: string;
}
