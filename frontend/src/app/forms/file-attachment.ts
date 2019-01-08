export interface SDFileAttachment extends File {
  id?: number;
  name: string;
  display_name?: string;
  url?: string;
  md5?: string;
  file_name?: string;
  date_modified?: Date;
  mime_type?: string;
  resource_id?: number;
}
