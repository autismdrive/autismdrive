
export interface Resource {
  id: number;
  title: string;
  type: string;
  description: string;
  image: string;
  imageCaption: string;
  organization: string;
  address: string;
  phone: string;
  website: string;
  categories: string[];
  status?: string;
}
