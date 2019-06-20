import { HitLabel } from './query';

export interface NewsItem {
  title: string;
  description: string;
  url: string;
  type?: HitLabel;
  img: string;
  imgClass?: string;
}
