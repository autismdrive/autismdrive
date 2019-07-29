export interface DataTransferLog {
  id: number;
  type: string;
  date_started: Date;
  last_updated: Date;
  total_records: number;
  alerts_sent: number;
  details: DataTransferDetail[];
}

export interface DataTransferDetail {
  id: number;
  date_started: Date;
  last_updated: Date;
  class_name: String;
  successful: boolean;
  success_count: boolean;
  failure_count: boolean;
  errors: String;
}

export interface DataTransferPageResults {
  pages: number;
  total: number;
  items: DataTransferLog[];
}

