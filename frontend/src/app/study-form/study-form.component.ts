import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../_services/api/api.service';
import { Study } from '../_models/study';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { FormGroup } from '@angular/forms';
import { Organization } from '../_models/organization';
import { Investigator } from '../_models/investigator';


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
        key: 'investigators',
        type: 'repeat',
        wrappers: ["card"],
        templateOptions: {
          label: 'Investigators',
            description: "Add an investigator",
        },
        fieldArray: {
          fieldGroup: [
            {
              key: 'name',
              type: 'input',
              templateOptions: {
                label: 'Full Name of Investigator',
                required: true,
              },
            },
            {
              key: 'title',
              type: 'input',
              templateOptions: {
                label: 'Title',
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
              key: 'bio_link',
              type: 'input',
              templateOptions: {
                label: 'Bio Link',
                placeholder: 'Please enter link to investigator bio',
              },
              validators: {"validation": ["url"]},
            },
          ],
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
        },
      },
      {
        key: 'eligibility_url',
        type: 'input',
        templateOptions: {
          label: 'Eligibility Link',
          placeholder: 'If you have an eligibilty screener, please enter the link',
        },
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

      if (params['studyId'] && params['studyType']) {
        const studyId = params['studyId'];
        const studyType = params['studyType'].charAt(0).toUpperCase() + params['studyType'].slice(1);
        this.createNew = false;
        this.model.createNew = false;
        this.api[`get${studyType}`](studyId).subscribe(study => {
          // this.study = new Study(study);
          this.model = this.study;
          this.loadStudyCategories(study, () => this.loadForm());
        });
      } else {
        this.createNew = true;
        this.model.createNew = true;
        // this.study = new Study({'title': '', 'description': '', 'participant_description': '', 'benefit_description': '',}) ;
        this.loadForm();
      }
    });
  }

  loadStudyCategories(study: Study, callback: Function) {
    this.model.categories = [];
    if (study.study_categories.length > 0) {
      for (const cat in study.study_categories) {
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
        console.log('we could add this category if it were hooked up:', this.model.categories[cat]);
        // this.api.addStudyCategory({study_id: this.study.id, category_id: Number(cat), type: this.study.type}).subscribe();
      }
    }
    // Remove any deleted categories
    for (const sc in this.study.study_categories) {
      if (!this.model.categories[this.study.study_categories[sc].category_id]) {
        console.log('we could delete this category if it were hooked up:', this.study.study_categories[sc]);
        // this.api.deleteStudyCategory(this.study.study_categories[rc]).subscribe();
      }
    }
  }

  addStudyCategories(study_id) {
    for (const cat in this.model.categories) {
      console.log('we could add this category if it were hooked up:', this.model.categories[cat]);
      // this.api.addStudyCategory({study_id: study_id, category_id: Number(cat), type: this.study.type}).subscribe();
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
    // Post to the study endpoint, and then close
    this.updateOrganization();
    if (this.form.valid) {
      if (this.createNew) {
        this.addAndClose(this.api.addStudy(this.model));
      } else {
        this.updateStudyCategories();
        this.updateAndClose(this.api.updateStudy(this.updatedModel));
      }
    }
  }

  addAndClose(apiCall) {
    apiCall.subscribe(s =>
      {
        this.updatedStudy = s;
        this.addStudyCategories(s.id);
        this.close();
      });
  }

  updateAndClose(apiCall) {
    apiCall.subscribe( s =>
      {
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
    })
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
