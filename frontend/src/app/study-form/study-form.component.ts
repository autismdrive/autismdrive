import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {Organization} from '../_models/organization';
import {Study} from '../_models/study';
import {StudyCategory} from '../_models/study_category';
import {StudyInvestigator} from '../_models/study_investigator';
import {ApiService} from '../_services/api/api.service';
import {scrollToFirstInvalidField} from '../../util/scrollToTop';
import {DeviceDetectorService} from 'ngx-device-detector';
import {AgeRange, Language} from '../_models/hit_type';


enum PageState {
  LOADING = 'loading',
  SHOW_FORM = 'form',
}

@Component({
  selector: 'app-study-form',
  templateUrl: './study-form.component.html',
  styleUrls: ['./study-form.component.scss']
})
export class StudyFormComponent implements OnInit {
  study: Study;
  updatedStudy: Study;
  pageState = PageState;
  state = PageState.LOADING;
  showConfirmDelete = false;

  model: any = {};
  form: FormGroup;
  fields: FormlyFieldConfig[] = [
    {
      key: 'status',
      type: 'select',
      templateOptions: {
        label: 'Study Status',
        placeholder: 'Please select the study status',
        options: [
          {'value': 'currently_enrolling', 'label': 'Currently Enrolling'},
          {'value': 'study_in_progress', 'label': 'Study in progress'},
          {'value': 'results_being_analyzed', 'label': 'Results being analyzed'},
          {'value': 'study_results_published', 'label': 'Study results published'}
        ],
        required: true,
      },
    },
    {
      key: 'title',
      type: 'input',
      templateOptions: {
        label: 'Title',
        placeholder: 'Please enter the title of your study',
        required: true,
      },
    },
    {
      key: 'short_title',
      type: 'input',
      templateOptions: {
        label: 'Short Title',
        placeholder: 'Please enter the short display title of your study',
        required: true,
        maxLength: 55,
      },
    },
    {
      key: 'description',
      type: 'textarea',
      templateOptions: {
        label: 'Description',
        placeholder: 'Please enter the description of your study',
        required: true,
      },
    },
    {
      key: 'short_description',
      type: 'textarea',
      templateOptions: {
        label: 'Short Description',
        placeholder: 'Please enter the short display description of your study',
        required: true,
        maxLength: 155,
      },
    },
    {
      key: 'participant_description',
      type: 'textarea',
      templateOptions: {
        label: 'Participant Description',
        placeholder: 'Who are you looking for to participate in your study?',
      },
      expressionProperties: {
        'templateOptions.required': 'model.status === "currently_enrolling"'
      }
    },
    {
      key: 'benefit_description',
      type: 'textarea',
      templateOptions: {
        label: 'Benefit Description',
        placeholder: 'How will participants benefit from your study?',
      },
      expressionProperties: {
        'templateOptions.required': 'model.status === "currently_enrolling"'
      }
    },
    {
      key: 'investigators',
      type: 'select',
      templateOptions: {
        label: 'Investigators',
        options: [],
        valueProp: 'id',
        labelProp: 'name',
        required: true,
        multiple: true,
      },
      hooks: {
        onInit: field => {
          field.templateOptions.options = this.api.getInvestigators();
        },
      },
    },
    {
      key: 'additional_investigators',
      wrappers: ['card'],
      templateOptions: {
        label: 'Additional Investigator',
        description: 'If your investigator does not appear in the list above, please add them here'
      },
      fieldGroup: [
        {
          type: 'input',
          key: 'name',
          templateOptions: {
            label: 'Name',
          },
        },
        {
          type: 'input',
          key: 'title',
          templateOptions: {
            label: 'Title',
          },
        },
        {
          type: 'select',
          key: 'organization',
          templateOptions: {
            label: 'Organization',
            options: [],
            valueProp: 'id',
            labelProp: 'name',
          },
          hooks: {
            onInit: field => {
              field.templateOptions.options = this.api.getOrganizations();
            },
          },
        },
        {
          type: 'input',
          key: 'bio_link',
          templateOptions: {
            label: 'Bio Link',
          },
        },
      ],
    },
    {
      key: 'organization',
      type: 'autocomplete',
      templateOptions: {
        label: 'Organization',
        filter: (term) => term ? this.filterOrganizations(term) : this.getOrganizations(),
      },
    },
    {
      key: 'location',
      type: 'input',
      templateOptions: {
        label: 'Location Name',
        placeholder: 'Please describe where the study will take place',
      },
    },
    {
      key: 'num_visits',
      type: 'input',
      templateOptions: {
        label: 'Number of Visits',
        type: 'number',
        placeholder: 'Please list the number of visits required for participation in this study',
      },
    },
    {
      key: 'coordinator_email',
      type: 'input',
      templateOptions: {
        label: 'Coordinator Email',
        placeholder: 'Please enter the email address to which study inquires will be sent',
      },
      expressionProperties: {
        'templateOptions.required': 'model.status === "currently_enrolling"'
      },
      validators: {'validation': ['email']},
    },
    {
      key: 'eligibility_url',
      type: 'input',
      templateOptions: {
        label: 'Eligibility Link',
        placeholder: 'If you have an eligibilty screener, please enter the link',
      },
      validators: {'validation': ['url']},
    },
    {
      key: 'results_url',
      type: 'input',
      templateOptions: {
        label: 'Results Url',
        placeholder: 'Link to published results of the study',
      },
      validators: {'validation': ['url']},
    },
    {
      key: 'image_url',
      type: 'input',
      templateOptions: {
        label: 'Image Url',
        placeholder: 'This is the link to the image used for current study display',
        description: 'Something like: /assets/home/study7.jpg'
      },
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
    },
    {
      key: 'ages',
      type: 'multicheckbox',
      templateOptions: {
        label: 'Age Ranges',
        type: 'array',
        options: this.getOptions(AgeRange.labels),
      },
    },
    {
      key: 'languages',
      type: 'multicheckbox',
      templateOptions: {
        label: 'Languages',
        type: 'array',
        options: this.getOptions(Language.labels),
      },
    },
  ];

  options: FormlyFormOptions;
  orgOptions: Organization[];

  createNew = false;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private deviceDetectorService: DeviceDetectorService,
  ) {
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

      if (params['studyId']) {
        const studyId = params['studyId'];
        this.createNew = false;
        this.model.createNew = false;
        this.api.getStudy(studyId).subscribe(study => {
          this.study = study as Study;
          this.model = this.study;
          this.loadInvestigators(study);
          this.loadStudyCategories(study, () => this.loadForm());
        });
      } else {
        this.createNew = true;
        this.model.createNew = true;
        this.study = {
          'title': '', 'description': '', 'participant_description': '', 'benefit_description': '',
          'investigators': [], 'location': '', 'categories': [], 'status': ''
        } as Study;
        this.loadForm();
      }
    });
  }

  loadInvestigators(study: Study) {
    this.model.investigators = [];
    if (study.study_investigators.length > 0) {
      study.study_investigators.forEach(inv => {
        this.model.investigators.push(inv.investigator.id);
      });
    }
  }

  loadStudyCategories(study: Study, callback: Function) {
    this.model.categories = [];
    if (study.study_categories.length > 0) {
      for (const cat of study.study_categories) {
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

  updateStudyCategories(study_id) {
    const selectedCategories: StudyCategory[] = [];
    this.model.categories.forEach((isSelected, i) => {
      if (isSelected === true) {
        selectedCategories.push({
          study_id: study_id,
          category_id: i,
        });
      }
    });
    return this.api.updateStudyCategories(study_id, selectedCategories);
  }

  addStudyInvestigator() {
    const addInvest = this.model.additional_investigators;
    const newInvest = {
      name: addInvest.name,
      title: addInvest.title,
      organization_id: addInvest.organization,
      bio_link: addInvest.bio_link,
    };
    return this.api.addInvestigator(newInvest);
  }

  updateStudyInvestigators(study_id) {
    const selectedInvestigators: StudyInvestigator[] = [];
    this.model.investigators.forEach(i => {
      selectedInvestigators.push({
        study_id: study_id,
        investigator_id: i,
      });
    });
    return this.api.updateStudyInvestigators(study_id, selectedInvestigators);
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
    // Post to the study endpoint, and then close
    if (this.form.valid) {
      if (this.createNew) {
        this.createNew = false;
        this.updateOrganization(() => this.updateAndClose(this.api.addStudy(this.model)));
      } else {
        this.updateOrganization(() => this.updateAndClose(this.api.updateStudy(this.model)));
      }
    }
  }

  updateAndClose(apiCall) {
    apiCall.subscribe(s => {
      this.updatedStudy = s;
      this.model.id = s.id;
      if (this.model.additional_investigators.name) {
        this.addStudyInvestigator().subscribe((i) => {
          this.model.investigators.push(i.id);
          this.updateStudyInvestigators(s.id).subscribe(() => {
            this.updateStudyCategories(s.id).subscribe(() => this.close());
          });
        });
      } else {
        this.updateStudyInvestigators(s.id).subscribe(() => {
          this.updateStudyCategories(s.id).subscribe(() => this.close());
        });
      }
    });
  }

  showDelete() {
    this.showConfirmDelete = true;
  }

  onDelete() {
    this.api.deleteStudy(this.study).subscribe(r => {
      this.router.navigate(['studies']);
    });
  }

  // Go to study screen
  close() {
    if (this.updatedStudy && this.updatedStudy.id) {
      this.router.navigate(['study', this.updatedStudy.id]);
    } else {
      this.router.navigate(['studies']);
    }
  }

  onCancel() {
    this.close();
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
