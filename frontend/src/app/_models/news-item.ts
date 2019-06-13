import { HitType } from './query';

export interface NewsItem {
  title: string;
  description: string;
  url: string;
  type?: HitType;
  img: string;
  imgClass?: string;
}
