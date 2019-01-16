import { TrainingCategory } from './training_category';

export interface Training {
  id: number;
  title: string;
  description: string;
  outcomes: string;
  image: string;
  imageCaption: string;
  status?: string;
  training_categories?: TrainingCategory[];
}
