import {ImportLog} from './import_log';

export interface ExportLog {
  id: number;
  last_updated: Date;
  available_records: number;
  alerts_sent: number;
}

export interface ExportLogPageResults {
  pages: number;
  total: number;
  items: ExportLog[];
}
