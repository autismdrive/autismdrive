import { User } from './user';

export interface Participant {

  id?: number;
  user_id: number;
  user: User;
  relationship: String;
  last_updated?: Date;
  percent_complete?: number;
  num_studies_enrolled?: number;
  avatar_img_url?: string;
  name?: string;

}
