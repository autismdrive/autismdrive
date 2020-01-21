import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ResourceCategory} from '../_models/resource_category';
import {ApiService} from '../_services/api/api.service';
import {Resource} from '../_models/resource';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {FormGroup} from '@angular/forms';
import {Organization} from '../_models/organization';


enum PageState {
  LOADING = 'loading',
  SHOW_FORM = 'form',
}

@Component({
  selector: 'app-resource-form',
  templateUrl: './resource-form.component.html',
  styleUrls: ['./resource-form.component.scss']
})
export class ResourceFormComponent implements OnInit {
  resource: Resource;
  updatedResource: Resource;
  pageState = PageState;
  state = PageState.LOADING;
  showConfirmDelete = false;

  model: any = {};
  form: FormGroup;
  fields: FormlyFieldConfig[] = [
    {
      key: 'type',
      type: 'select',
      templateOptions: {
        label: 'Type',
        options: [
          {'value': 'resource', 'label': 'Online Information'},
          {'value': 'location', 'label': 'Local Services'},
          {'value': 'event', 'label': 'Events and Training'}
        ],
        required: true,
      },
      hideExpression: '!model.createNew',
    },
    {
      key: 'title',
      type: 'input',
      templateOptions: {
        label: 'Title',
        placeholder: 'Please enter the title',
        required: true,
      },
      expressionProperties: {
        'templateOptions.placeholder': '"Please enter the title of your " + (model.type || "resource")',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'description',
      type: 'textarea',
      templateOptions: {
        label: 'Description',
        placeholder: 'Please enter a description',
        required: true,
      },
      expressionProperties: {
        'templateOptions.placeholder': '"Please enter a description of your " + (model.type || "resource")',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'date',
      type: 'datepicker',
      templateOptions: {
        label: 'Event Date',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'time',
      type: 'input',
      templateOptions: {
        label: 'Event Time',
        placeholder: 'Please enter the start time or time-frame for your event',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'ticket_cost',
      type: 'input',
      templateOptions: {
        label: 'Event Ticket Cost',
        placeholder: 'Please enter the ticket cost for your event',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'organization',
      type: 'autocomplete',
      templateOptions: {
        label: 'Organization',
        filter: (term) => term ? this.filterOrganizations(term) : this.getOrganizations(),
      },
      hideExpression: '!model.type',
    },
    {
      key: 'primary_contact',
      type: 'input',
      templateOptions: {
        label: 'Primary Contact',
        placeholder: 'Please enter the primary contact for your location or event',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'contact_email',
      type: 'input',
      templateOptions: {
        label: 'Contact Email',
        placeholder: 'This contact email will not be displayed on the site and is intended for admin use only',
      },
      validators: {'validation': ['email']},
      hideExpression: '!model.type',
    },
    {
      key: 'location_name',
      type: 'input',
      templateOptions: {
        label: 'Location Name',
        placeholder: 'Please enter the name for your event venue',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'street_address1',
      type: 'input',
      templateOptions: {
        label: 'Street Address',
        placeholder: 'Please enter the street address',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'street_address2',
      type: 'input',
      templateOptions: {
        label: 'Street Address Details',
        placeholder: 'Please enter any additional details for the street address',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'city',
      type: 'input',
      templateOptions: {
        label: 'City',
        placeholder: 'Please enter the city',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'state',
      type: 'input',
      templateOptions: {
        label: 'State',
        placeholder: 'Please enter the state',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'zip',
      type: 'input',
      templateOptions: {
        label: 'Zip Code',
        placeholder: 'Please enter the zip code',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'phone',
      type: 'input',
      templateOptions: {
        label: 'Phone Number',
        placeholder: 'Please enter the phone number',
      },
      hideExpression: '!model.type',
      validators: {'validation': ['phone']},
    },
    {
      key: 'website',
      type: 'input',
      templateOptions: {
        label: 'Website',
        placeholder: 'Please enter the website',
      },
      hideExpression: '!model.type',
      validators: {'validation': ['url']},
    },
    {
      key: 'video_code',
      type: 'input',
      templateOptions: {
        label: 'Video Code',
        placeholder: 'Please enter the YouTube code for a video of this content',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'is_uva_education_content',
      type: 'radio',
      templateOptions: {
        label: 'UVA Education Content',
        placeholder: 'Should this resource be displayed on the UVA Education page?',
        options: [
          {value: true, label: 'Yes'},
          {value: false, label: 'No'},
        ]
      },
      hideExpression: '!model.type',
    },
    {
      key: 'categories',
      type: 'multiselecttree',
      templateOptions: {
        label: 'Topics',
        options: this.api.getCategoryTree(),
        valueProp: 'id',
        labelProp: 'name',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'ages',
      type: 'multicheckbox',
      templateOptions: {
        label: 'Age Ranges',
        type: 'array',
        options: [
          {'value': 'pre-k', 'label': 'Pre-K (0 - 5 years)'},
          {'value': 'school', 'label': 'School age (6 - 13 years)'},
          {'value': 'transition', 'label': 'Transition age (14 - 22 years)'},
          {'value': 'adult', 'label': 'Adulthood (23 - 64)'},
          {'value': 'aging', 'label': 'Aging (65+)'}
        ],
      },
      hideExpression: '!model.type',
    },
  ];

  options: FormlyFormOptions;
  orgOptions: Organization[];

  createNew = false;

  constructor(private api: ApiService,
              private route: ActivatedRoute,
              private router: Router) {
    this.getOrganizations();
  }

  ngOnInit() {
    this.model.createNew = false;
    this.loadData();
  }

  getOrganizations() {
    this.api.getOrganizations().subscribe(orgs => {
        return this.orgOptions = orgs;
      }
    );
  }

  filterOrganizations(name: string): Organization[] {
    return this.orgOptions.filter(org =>
      org.name.toLowerCase().includes(name.toLowerCase())
    );
  }

  loadData() {
    this.route.params.subscribe(params => {

      if (params['resourceId'] && params['resourceType']) {
        const resourceId = params['resourceId'];
        const resourceType = params['resourceType'].charAt(0).toUpperCase() + params['resourceType'].slice(1);
        this.createNew = false;
        this.model.createNew = false;
        this.api[`get${resourceType}`](resourceId).subscribe(resource => {
          this.resource = new Resource(resource);
          this.model = this.resource;
          this.loadResourceCategories(resource, () => this.loadForm());
        });
      } else {
        this.createNew = true;
        this.model.createNew = true;
        this.resource = new Resource({'type': '', 'title': '', 'description': '', 'phone': '', 'website': ''});
        this.loadForm();
      }
    });
  }

  loadResourceCategories(resource: Resource, callback: Function) {
    this.model.categories = [];
    if (resource.resource_categories.length > 0) {
      for (const cat of resource.resource_categories) {
        this.model.categories.push(cat.category);
        callback();
      }
    } else {
      callback();
    }
  }

  loadForm() {
    this.form = new FormGroup({});
    this.options = {
      formState: {
        mainModel: this.model
      }
    };
    this.state = this.pageState.SHOW_FORM;
  }

  updateResourceCategories(resource_id) {
    const selectedCategories: ResourceCategory[] = [];
    this.model.categories.forEach((isSelected, i) => {
      if (isSelected === true) {
        selectedCategories.push({
          resource_id: resource_id,
          category_id: i,
          type: this.model.type
        });
      }
    });
    return this.api.updateResourceCategories(resource_id, selectedCategories);
  }

  updateOrganization(callback: Function) {
    // If the user selects an existing Organization name from the list, it will be saved as an Organization object. If they write in their
    // own Organization name, it will be saved as a new organization with that name. When saving a new organization, we also create an
    // updated model so that we don't accidentally save the old version before it's updated. When there is no Organization being saved, all
    // we do is create the updated model.
    if (this.model.organization) {
      if (this.model.organization.constructor.name === 'String') {
        this.api.addOrganization({name: this.model.organization}).subscribe(org => {
          this.model.organization_id = org.id;
          this.model.organization = org;
          callback();
        });
      } else {
        this.model.organization_id = this.model.organization.id;
        callback();
      }
    } else {
      callback();
    }
  }

  submit() {
    // Post to the resource endpoint, and then close
    const resourceType = this.model.type.charAt(0).toUpperCase() + this.model.type.slice(1);

    if (this.form.valid) {
      if (this.createNew) {
        this.updateOrganization(() => this.updateAndClose(this.api[`add${resourceType}`](this.model)));
      } else {
        this.updateOrganization(() => this.updateAndClose(this.api[`update${resourceType}`](this.model)));
      }
    }
  }

  updateAndClose(apiCall) {
    apiCall.subscribe(r => {
      this.updatedResource = r;
      this.updateResourceCategories(r.id).subscribe(() => this.close());
    });
  }

  showDelete() {
    this.showConfirmDelete = true;
  }

  onDelete() {
    this.api.deleteResource(this.resource).subscribe(r => {
      this.router.navigate(['search']);
    });
  }

  // Go to resource screen
  close() {
    if (this.updatedResource && this.updatedResource.id) {
      this.router.navigate([this.updatedResource.type, this.updatedResource.id]);
    } else {
      this.router.navigate(['search']);
    }
  }

  onCancel() {
    this.close();
  }
}
