import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ResourceCategory} from '../_models/resource_category';
import {ApiService} from '../_services/api/api.service';
import {Resource} from '../_models/resource';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {AbstractControl, FormGroup} from '@angular/forms';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/api/authentication-service';
import {scrollToFirstInvalidField} from '../../util/scrollToTop';
import {DeviceDetectorService} from 'ngx-device-detector';
import {AgeRange, Language, Covid19Categories} from '../_models/hit_type';


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
  currentUser: User;

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
          {'value': 'event', 'label': 'Events and Training'},
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
      key: 'insurance',
      type: 'textarea',
      templateOptions: {
        label: 'Insurance',
        placeholder: 'Please enter the type of insurance if applicable (e.g., private, medicaid, Tricare)',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'includes_registration',
      type: 'radio',
      defaultValue: false,
      templateOptions: {
        label: 'Allow Registration',
        description: 'Should users be able to register for this event through Autism DRIVE?',
        options: [
          {value: true, label: 'Yes'},
          {value: false, label: 'No'},
        ]
      },
      expressionProperties: {
        'templateOptions.required': 'model.type === "event"'
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'registration_url',
      type: 'input',
      templateOptions: {
        label: 'Registration Link',
        placeholder: 'http://link.to/external/website',
        type: 'url',
      },
      expressionProperties: {
        'templateOptions.required': 'model.type === "event" && !model.includes_registration'
      },
      hideExpression: '!(model.type === "event" && !model.includes_registration)',
    },
    {
      key: 'image_url',
      type: 'input',
      templateOptions: {
        label: 'Feature Image',
        placeholder: 'http://link.to/file.jpg',
        type: 'url',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'date',
      type: 'datepicker',
      templateOptions: {
        label: 'Event Date',
      },
      expressionProperties: {
        'templateOptions.required': 'model.type === "event"'
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
      expressionProperties: {
        'templateOptions.required': 'model.type === "event"'
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
      key: 'webinar_link',
      type: 'input',
      templateOptions: {
        label: 'Webinar Link',
        placeholder: 'Please enter the link to attend the webinar',
      },
      hideExpression: 'model.type != "event"',
      validators: {'validation': ['url']},
    },
    {
      key: 'post_survey_link',
      type: 'input',
      templateOptions: {
        label: 'Survey Link',
        placeholder: 'Please enter the link to the post-event survey',
      },
      hideExpression: 'model.type != "event"',
      validators: {'validation': ['url']},
    },
    {
      key: 'max_users',
      type: 'input',
      templateOptions: {
        label: 'Maximum attendees',
        placeholder: 'Please enter the maximum number of users allowed to register',
        type: 'number'
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'organization_name',
      type: 'input',
      templateOptions: {
        label: 'Organization Name',
        placeholder: 'Please enter the name of the organization for your resource',
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
      key: 'phone_extension',
      type: 'input',
      templateOptions: {
        label: 'Phone Number Extension',
        placeholder: 'Please enter any extension to the phone number',
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
      defaultValue: false,
      templateOptions: {
        label: 'UVA Education Content',
        description: 'Should this resource be displayed on the UVA Education page?',
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
        description: 'This field is required',
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
        options: this.getOptions(AgeRange.labels),
      },
      hideExpression: '!model.type',
    },
    {
      key: 'languages',
      type: 'multicheckbox',
      templateOptions: {
        label: 'Languages',
        type: 'array',
        options: this.getOptions(Language.labels),
      },
      hideExpression: '!model.type',
    },
    {
      key: 'covid19_categories',
      type: 'multicheckbox',
      templateOptions: {
        label: 'COVID-19 Topics',
        type: 'array',
        options: this.getOptions(Covid19Categories.labels),
      },
      hideExpression: '!model.type',
    },
    {
      key: 'should_hide_related_resources',
      type: 'radio',
      defaultValue: false,
      templateOptions: {
        label: 'Hide Related Resources',
        description: 'Should related resources be displayed alongside this resource on the details page?',
        options: [
          {value: true, label: 'Yes'},
          {value: false, label: 'No'},
        ]
      },
      hideExpression: '!model.type',
    },
  ];



  options: FormlyFormOptions;

  createNew = false;

  constructor(private api: ApiService,
              private route: ActivatedRoute,
              private router: Router,
              private authenticationService: AuthenticationService,
              private deviceDetectorService: DeviceDetectorService,
              ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);

  }

  ngOnInit() {
    this.model.createNew = false;
    this.loadData();
  }

  getOptions(modelLabels) {
    const opts = [];
    for (const key in modelLabels) {
      if (modelLabels.hasOwnProperty(key)) {
        opts.push({'value': key, 'label': modelLabels[key]});
      }
    }
    return opts;
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
        this.model.categories = [];
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
    const resourceType = this.model.type.charAt(0).toUpperCase() + this.model.type.slice(1);

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
    return this.api[`update${resourceType}Categories`](resource_id, selectedCategories);
  }

  submit() {
    // Post to the resource endpoint, and then close
    const resourceType = this.model.type.charAt(0).toUpperCase() + this.model.type.slice(1);

    if (this.form.valid) {
      if (this.createNew && !this.model.id) {
        this.updateAndClose(this.api[`add${resourceType}`](this.model));
      } else {
        this.updateAndClose(this.api[`update${resourceType}`](this.model));
      }
    }
  }

  updateAndClose(apiCall) {
    this.setDateTime();
    apiCall.subscribe(r => {
      this.updatedResource = r;
      this.model.id = r.id;
      this.updateResourceCategories(r.id).subscribe(() => this.close());
    });
  }

  setDateTime() {
    if (this.model.date) {
      if (this.model.date instanceof Date) {
          this.model.date.setHours(12);
      } else {
        this.model.date = new Date(this.model.date);
        this.model.date.setHours(12);
      }
    }
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

  saveDraft() {
    this.model.is_draft = true;
    this.form.valid ? this.submit() : this.highlightRequiredFields();
  }

  savePublish() {
    this.model.is_draft = false;
    this.form.valid ? this.submit() : this.highlightRequiredFields();
  }


  highlightRequiredFields() {
    for (const fieldName of Object.keys(this.form.controls)) {
      const field: AbstractControl = this.form.controls[fieldName];
      field.updateValueAndValidity();
      field.markAsDirty();
    }

    scrollToFirstInvalidField(this.deviceDetectorService);
  }
}
