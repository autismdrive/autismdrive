import { User } from './user';

export interface Participant {
  id: number;
  last_updated: Date;
  first_name: string;
  last_name: string;
  users: User[];

  // first_name: string;
  // nickname: string;
  // last_name: string;
  // relationship: string;
  // percent_complete: number;
  // num_studies_enrolled: number;
  // avatar_img_url: string;

}
