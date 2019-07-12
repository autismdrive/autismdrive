import { ResourceCategory } from './resource_category';
import { Organization } from './organization';
import { GeoLocation } from './geolocation';
import { Category } from './category';

export class Resource extends GeoLocation {
  id?: number;
  type: string;
  title: string;
  description: string;
  date?: string;
  time?: string;
  ticket_cost?: string;
  organization?: Organization;
  organization_id?: number;
  primary_contact?: string;
  location_name?: string;
  street_address1?: string;
  street_address2?: string;
  city?: string;
  state?: string;
  zip?: string;
  phone: string;
  website: string;
  last_updated?: string;
  status?: string;
  resource_categories?: ResourceCategory[];
  categories?: Category[];

  constructor(private _props) {
    super(_props);

    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
}
