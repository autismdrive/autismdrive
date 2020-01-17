import {Component, OnInit} from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {FormlyFieldConfig, FormlyFormOptions} from '@ngx-formly/core';
import {Organization} from '../_models/organization';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';


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
  updatedModel: any = {};
  form: FormGroup;
  fields: FormlyFieldConfig[] = [
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
        required: true,
      },
    },
    {
      key: 'benefit_description',
      type: 'textarea',
      templateOptions: {
        label: 'Benefit Description',
        placeholder: 'How will participants benefit from your study?',
        required: true,
      },
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
      key: 'coordinator_email',
      type: 'input',
      templateOptions: {
        label: 'Coordinator Email',
        placeholder: 'Please enter the email address to which study inquires will be sent',
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
      key: 'image_url',
      type: 'input',
      templateOptions: {
        label: 'Image Url',
        placeholder: 'This is the link to the image used for current study display',
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
        options: [
          {'value': 'pre-k', 'label': 'Pre-K (0 - 5 years)'},
          {'value': 'school', 'label': 'School age (6 - 13 years)'},
          {'value': 'transition', 'label': 'Transition age (14 - 22 years)'},
          {'value': 'adult', 'label': 'Adulthood (23 - 64)'},
          {'value': 'aging', 'label': 'Aging (65+)'}
        ],
      },
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

      if (params['studyId']) {
        const studyId = params['studyId'];
        this.createNew = false;
        this.model.createNew = false;
        this.api.getStudy(studyId).subscribe(study => {
          this.study = study as Study;
          this.model = this.study;
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

  loadStudyCategories(study: Study, callback: Function) {
    this.model.categories = [];
    if (study.study_categories.length > 0) {
      for (const cat of Object.keys(study.study_categories)) {
        this.model.categories[study.study_categories[cat].category.id] = true;
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

  updateStudyCategories() {
    const scIds = this.study.study_categories.map(sc => sc.category.id);
    // Add the new categories
    for (const cat in this.model.categories) {
      if (!scIds.includes(Number(cat))) {
        this.api.addStudyCategory({study_id: this.study.id, category_id: Number(cat)}).subscribe();
      }
    }
    // Remove any deleted categories
    for (const sc in this.study.study_categories) {
      if (!this.model.categories[this.study.study_categories[sc].category_id]) {
        this.api.deleteStudyCategory(this.study.study_categories[sc]).subscribe();
      }
    }
  }

  addStudyCategories(study_id) {
    for (const cat of Object.keys(this.model.categories)) {
      this.api.addStudyCategory({
        study_id: study_id,
        category_id: parseInt(cat, 10)
      }).subscribe();
    }
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
          this.updatedModel = this.model;
          callback();
        });
      } else {
        this.model.organization_id = this.model.organization.id;
        this.updatedModel = this.model;
        callback();
      }
    } else {
      this.updatedModel = this.model;
      callback();
    }
  }

  submit() {
    // Post to the study endpoint, and then close
    if (this.form.valid) {
      if (this.createNew) {
        this.updateOrganization(() => this.addAndClose());
      } else {
        this.updateStudyCategories();
        this.updateOrganization(() => this.updateAndClose());
      }
    }
  }

  addAndClose() {
    this.api.addStudy(this.model).subscribe(s => {
      this.updatedStudy = s;
      this.addStudyCategories(s.id);
      this.close();
    });
  }

  updateAndClose() {
    this.api.updateStudy(this.updatedModel).subscribe(s => {
      this.updatedStudy = s;
      this.close();
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
}
