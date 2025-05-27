import {HitType} from './hit_type';

export interface NewsItem {
  title: string;
  description: string;
  url: string;
  type?: HitType;
  img: string;
  imgClass?: string;
  label?: string;
}
