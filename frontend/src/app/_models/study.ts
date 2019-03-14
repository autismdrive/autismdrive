import { StudyCategory } from './study_category';

export interface Study {
  id: number;
  title: string;
  description: string;
  researcher_description: string;
  participant_description: string;
  outcomes: string;
  enrollment_start_date: string;
  enrollment_end_date: string;
  current_num_participants: number;
  max_num_participants: number;
  start_date: string;
  end_date: string;
  categories: string[];
  status?: string;
  study_categories?: StudyCategory[];
}
