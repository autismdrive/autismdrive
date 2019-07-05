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
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'ticket_cost',
      type: 'input',
      templateOptions: {
        label: 'Event Ticket Cost',
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
    this.loadForm();
  }

  loadForm() {
    // this.fields = this.infoToForm();
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
        this.api.addResource(this.model).subscribe();
        this.close();
      } else {
        this.api.updateResource(this.model).subscribe();
        this.close();
      }
    }
  }

  // Go to resource screen
  close() {
    if (this.resource && this.resource.id) {
      this.router.navigate(['resource', this.resource.id]);
    } else {
      this.router.navigate(['resources']);
    }
  }

  onCancel() {
    this.close();
  }
}
