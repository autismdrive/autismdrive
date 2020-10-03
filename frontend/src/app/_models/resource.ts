import { ResourceCategory } from './resource_category';
import { GeoLocation } from './geolocation';
import { Category } from './category';

export class Resource extends GeoLocation {
  id?: number;
  type: string;
  title: string;
  description: string;
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

  constructor(private _props) {
    super(_props);

    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
