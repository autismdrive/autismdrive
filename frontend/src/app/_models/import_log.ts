export interface ImportLog {
  id: number;
  date_started: Date;
  last_updated: Date;
  class_name: number;
  successful: boolean;
  success_count: number;
  failure_count: number;
  errors: string;
}

export interface ImportLogPageResults {
  pages: number;
  total: number;
  items: ImportLog[];
}
