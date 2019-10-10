import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../_services/api/api.service';
import { Resource } from '../_models/resource';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { FormGroup } from '@angular/forms';
import { Organization } from '../_models/organization';


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
  updatedModel: any = {};
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
          "templateOptions.placeholder": '"Please enter the title of your " + (model.type || "resource")',
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
          "templateOptions.placeholder": '"Please enter a description of your " + (model.type || "resource")',
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
        validators: {"validation": ["phone"]},
      },
      {
        key: 'website',
        type: 'input',
        templateOptions: {
          label: 'Website',
          placeholder: 'Please enter the website',
        },
        hideExpression: '!model.type',
        validators: {"validation": ["url"]},
      },
      {
        key: 'categories',
        type: 'multicheckbox',
        templateOptions: {
          label: 'Topics',
          options: this.api.getCategories(),
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
          type: "array",
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

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.getOrganizations();
  }

  ngOnInit() {
    this.model.createNew = false;
    this.loadData();
  }

  getOrganizations() {
    this.api.getOrganizations().subscribe( orgs => {
       return this.orgOptions = orgs;
      }
    )
  }

  filterOrganizations(name: string): Organization[] {
    return this.orgOptions.filter(org =>
      org.name.toLowerCase().includes(name.toLowerCase())
    )
  }

  loadData() {
    this.route.params.subscribe(params => {
      const resourceId = params['resourceId'];
      const resourceType = params['resourceType'].charAt(0).toUpperCase() + params['resourceType'].slice(1);

      if (resourceId && resourceType) {
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
        this.resource = new Resource({'type': '', 'title': '', 'description': '', 'phone': '', 'website': '' }) ;
        this.loadForm();
      }
    });
  }

  loadResourceCategories(resource: Resource, callback: Function) {
    this.model.categories = [];
    if (resource.resource_categories.length > 0) {
      for (const cat in resource.resource_categories) {
        this.model.categories[resource.resource_categories[cat].category.id] = true;
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

  updateResourceCategories() {
    const rcIds = this.resource.resource_categories.map(rc => rc.category.id);
    // Add the new categories
    for (const cat in this.model.categories) {
      if (!rcIds.includes(Number(cat))) {
        this.api.addResourceCategory({resource_id: this.resource.id, category_id: Number(cat), type: this.resource.type}).subscribe();
      }
    }
    // Remove any deleted categories
    for (const rc in this.resource.resource_categories) {
      if (!this.model.categories[this.resource.resource_categories[rc].category_id]) {
        this.api.deleteResourceCategory(this.resource.resource_categories[rc]).subscribe();
      }
    }
  }

  addResourceCategories(resource_id) {
    for (const cat in this.model.categories) {
      this.api.addResourceCategory({resource_id: resource_id, category_id: Number(cat), type: this.resource.type}).subscribe();
    }
  }

  updateOrganization() {
    // If the user selects an existing Organization name from the list, it will be saved as an Organization object. If they write in their
    // own Organization name, it will be saved as a new organization with that name. When saving a new organization, we also create an
    // updated model so that we don't accidentally save the old version before it's updated. When there is no Organization being saved, all
    // we do is create the updated model.
    if (this.model.organization){
      if (this.model.organization.constructor.name == "String") {
        this.api.addOrganization({name: this.model.organization}).subscribe( org => {
          this.model.organization_id = org.id;
          this.model.organization = org;
          this.updatedModel = this.model;
          this.submit();
        })
      } else {
        this.model.organization_id = this.model.organization.id;
        this.updatedModel = this.model;
      }
    } else {
      this.updatedModel = this.model;
    }
  }

  submit() {
    // Post to the resource endpoint, and then close
    this.updateOrganization();
    if (this.form.valid) {
      if (this.createNew) {
        if (this.model.type == 'resource') {
          this.addAndClose(this.api.addResource(this.model));
        } else if (this.model.type == 'location') {
          this.addAndClose(this.api.addLocation(this.model));
        } else if (this.model.type == 'event') {
          this.addAndClose(this.api.addEvent(this.model));
        }
      } else {
        this.updateResourceCategories();
        if (this.model.type == 'resource') {
          this.updateAndClose(this.api.updateResource(this.updatedModel));
        } else if (this.model.type == 'location') {
          this.updateAndClose(this.api.updateLocation(this.updatedModel));
        } else if (this.model.type == 'event') {
          this.updateAndClose(this.api.updateEvent(this.updatedModel));
        }
      }
    }
  }

  addAndClose(apiCall) {
    apiCall.subscribe(r =>
      {
        this.updatedResource = r;
        this.addResourceCategories(r.id);
        this.close();
      });
  }

  updateAndClose(apiCall) {
    apiCall.subscribe( r =>
      {
        this.updatedResource = r;
        this.close();
      });
  }

  showDelete() {
    this.showConfirmDelete = true;
  }

  onDelete() {
    this.api.deleteResource(this.resource).subscribe(r => {
      this.router.navigate(['search']);
    })
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
