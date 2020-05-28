import {Component, OnInit} from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Covid19Categories} from '../_models/hit_type';
import {Hit, Query} from '../_models/query';
import {Resource} from '../_models/resource';
import {User} from '../_models/user';
import {AuthenticationService} from '../_services/api/authentication-service';

interface C19ResourceCategoryObj {
  name: string;
  label: string;
  description: string;
}

@Component({
  selector: 'app-covid19-resources',
  templateUrl: './covid19-resources.component.html',
  styleUrls: ['./covid19-resources.component.scss']
})
export class Covid19ResourcesComponent implements OnInit {
  query: Query;
  C19Categories: C19ResourceCategoryObj[];
  selectedCategory: C19ResourceCategoryObj;
  resourceHits: Hit[];
  currentUser: User;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {
    this.C19Categories = Object.keys(Covid19Categories.labels).map(k => {
      return {
        name: k,
        label: Covid19Categories.labels[k].split(': ')[0],
        description: Covid19Categories.labels[k].split(': ')[1]
      };
    });
    this.route.params.subscribe(params => {
      if ('category' in params) {
        this.selectedCategory = this.C19Categories.find(x => x.name === params['category']);
      } else {
        this.selectedCategory = this.C19Categories[0];
        this.route.params['category'] = this.C19Categories[0].name;
        this.router.navigate(['/covid19-resources/' + this.C19Categories[0].name]);
      }
    });
    this.loadResources();
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  ngOnInit() {
  }

  loadResources() {
    this.api.getCovid19ResourcesByCategory(this.selectedCategory.name).subscribe(resources => {
      this.resourceHits = this._resourcesToHits(resources);
    });
  }

  selectCategory(category: C19ResourceCategoryObj) {
    this.selectedCategory = category;
    this.router.navigate(['/covid19-resources/' + category.name]);
    this.loadResources();
  }

   private _resourcesToHits(resources: Resource[]): Hit[] {
      return resources
        .map(r => {
          return new Hit({
            id: r.id,
            type: 'resource',
            ages: r.ages,
            title: r.title,
            content: r.description,
            description: r.description,
            last_updated: r.last_updated,
            highlights: null,
            url: `/resource/${r.id}`,
            label: 'Research Studies',
            status: this.C19Categories.find(cat => r.covid19_categories.includes(cat.name)).label
          });
        });
  }

}
