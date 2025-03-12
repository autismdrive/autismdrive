import {NgIf} from '@angular/common';
import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {ActivatedRoute, Router} from '@angular/router';
import {LoadingComponent} from '@app/loading/loading.component';
import {getResourceFormFields} from '@app/resource-form/resource-form.fields';
import {Resource, ResourceType} from '@models/resource';
import {ResourceCategory} from '@models/resource_category';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {FormlyFieldConfig, FormlyFormOptions, FormlyModule} from '@ngx-formly/core';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';
import {scrollToFirstInvalidField} from '@util/scrollToTop';
import {DeviceDetectorService} from 'ngx-device-detector';

enum PageState {
  LOADING = 'loading',
  SHOW_FORM = 'form',
}

@Component({
  standalone: true,
  selector: 'app-resource-form',
  templateUrl: './resource-form.component.html',
  styleUrls: ['./resource-form.component.scss'],
  imports: [LoadingComponent, NgIf, FormlyModule, ReactiveFormsModule, FlexModule, MatButtonModule],
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
  fields: FormlyFieldConfig[];
  options: FormlyFormOptions;
  createNew = false;

  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
    private deviceDetectorService: DeviceDetectorService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
    this.fields = getResourceFormFields(this.api.getCategoryTree());
  }

  ngOnInit() {
    this.model.createNew = false;
    this.loadData();
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
        this.resource = new Resource({type: ResourceType.RESOURCE, title: '', description: '', phone: '', website: ''});
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
        mainModel: this.model,
      },
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
          type: this.model.type,
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
