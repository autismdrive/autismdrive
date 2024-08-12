import {Category} from './category';
import {GeoLocation} from './geolocation';
import {ResourceCategory} from './resource_category';

export enum ResourceType {
  RESOURCE = 'resource',
  EVENT = 'event',
  LOCATION = 'location',
}

export interface ResourceProps {
  type: ResourceType;
  title: string;
  description: string;
  post_event_description: string;
  insurance: string;
  date?: string;
  time?: string;
  ticket_cost?: string;
  organization_name?: string;
  primary_contact?: string;
  location_name?: string;
  street_address1?: string;
  street_address2?: string;
  city?: string;
  state?: string;
  zip?: string;
  phone?: string;
  phone_extension?: string;
  website?: string;
  contact_email?: string;
  video_code?: string;
  is_uva_education_content?: boolean;
  is_draft?: boolean;
  last_updated?: string;
  status?: string;
  resource_categories?: ResourceCategory[];
  categories?: Category[];
  ages?: string[];
  languages?: string[];
  covid19_categories?: string[];
  includes_registration?: boolean;
  webinar_link?: string;
  post_survey_link?: string;
  max_users?: number;
  image_url?: string;
  registration_url?: string;
  should_hide_related_resources?: boolean;
}

export class Resource extends GeoLocation {
  type: ResourceType;
  title: string;
  description: string;
  post_event_description: string;
  insurance: string;
  date?: string;
  time?: string;
  ticket_cost?: string;
  organization_name?: string;
  primary_contact?: string;
  location_name?: string;
  street_address1?: string;
  street_address2?: string;
  city?: string;
  state?: string;
  zip?: string;
  phone?: string;
  phone_extension?: string;
  website?: string;
  contact_email?: string;
  video_code?: string;
  is_uva_education_content?: boolean;
  is_draft?: boolean;
  last_updated?: string;
  status?: string;
  resource_categories?: ResourceCategory[];
  categories?: Category[];
  ages?: string[];
  languages?: string[];
  covid19_categories?: string[];
  includes_registration?: boolean;
  webinar_link?: string;
  post_survey_link?: string;
  max_users?: number;
  image_url?: string;
  registration_url?: string;
  should_hide_related_resources?: boolean;

  constructor(private _props: Partial<ResourceProps>) {
    super(_props);

    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
