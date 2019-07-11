import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../_services/api/api.service';
import { Resource } from '../_models/resource';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { FormGroup } from '@angular/forms';


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
  pageState = PageState;
  state = PageState.LOADING;

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
        type: 'select',
        templateOptions: {
          label: 'Organization',
          options: []
        },
        hideExpression: '!model.type',
        expressionProperties: {
          'templateOptions.options': this.api.getOrganizations()
        },
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
      },
      {
        key: 'website',
        type: 'input',
        templateOptions: {
          label: 'Website',
          placeholder: 'Please enter the website',
        },
        hideExpression: '!model.type',
      },
      {
        key: 'resource_categories',
        type: 'multicheckbox',
        templateOptions: {
          label: 'Topics',
          options: [],
        },
        hideExpression: '!model.type',
        expressionProperties: {
          'templateOptions.options': this.api.getCategories()
        }
      },
    ];

  options: FormlyFormOptions;

  createNew = false;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.route.params.subscribe(params => {
      const resourceId = params['resourceId'];
      const resourceType = params['resourceType'];

      if (resourceId) {
        this.createNew = false;
          if (resourceType == 'resource') {
            this.api
              .getResource(resourceId)
              .subscribe(resource => {
                this.resource = resource;
                this.model = resource;
                this.loadResourceCategories(resource, () => this.loadForm());
              });
          } else if (resourceType == 'location') {
            this.api
              .getLocation(resourceId)
              .subscribe(resource => {
                this.resource = resource;
                this.model = resource;
                this.loadResourceCategories(resource, () => this.loadForm());
              });
          } else if (resourceType == 'event') {
            this.api
              .getEvent(resourceId)
              .subscribe(resource => {
                this.resource = resource;
                this.model = resource;
                this.loadResourceCategories(resource, () => this.loadForm());
              });
          }
      } else {
        this.createNew = true;
        this.loadForm();
      }
    });
  }

  loadResourceCategories(resource: Resource, callback: Function) {
    this.api
      .getResourceCategories(resource)
      .subscribe(rcs => {
        this.model.resource_categories = rcs;
        callback();
      });
}

  loadForm() {
    console.log('Model: ', this.model);
    console.log('Fields: ', this.fields);

    this.form = new FormGroup({});
    this.options = {
      formState: {
        mainModel: this.model
      }
    };
    this.state = this.pageState.SHOW_FORM;
  }

  submit() {
    // Post to the resource endpoint, and then close
    if (this.form.valid) {
      if (this.createNew) {
        if (this.model.type == 'resource') {
          this.api.addResource(this.model).subscribe();
        } else if (this.model.type == 'location') {
          this.api.addLocation(this.model).subscribe();
        } else if (this.model.type == 'event') {
          this.api.addEvent(this.model).subscribe();
        }
        this.close();
      } else {
        if (this.model.type == 'resource') {
          this.api.updateResource(this.model).subscribe();
        } else if (this.model.type == 'location') {
          this.api.updateLocation(this.model).subscribe();
        } else if (this.model.type == 'event') {
          this.api.updateEvent(this.model).subscribe();
        }

        this.close();
      }
    }
  }

  // Go to resource screen
  close() {
    if (this.resource && this.resource.id) {
      this.router.navigate([this.resource.type, this.resource.id]);
    } else {
      this.router.navigate(['resources']);
    }
  }

  onCancel() {
    this.close();
  }
}
