import {Component, OnInit} from '@angular/core';
import {HitType} from '../_models/hit_type';
import {NewsItem} from '../_models/news-item';
import {Resource} from '../_models/resource';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';

@Component({
  selector: 'app-uva-education',
  templateUrl: './uva-education.component.html',
  styleUrls: ['./uva-education.component.scss']
})
export class UvaEducationComponent implements OnInit {
  edResources: Resource[];
  newsItems: NewsItem[];
  currentUser: User;
  loading = true;


  constructor(
    private api: ApiService,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.loadResources();
  }

  ngOnInit() {
  }

  loadResources() {
    this.api.getResources().subscribe(resources => {
      this.edResources = resources.filter(r => r.is_uva_education_content === true);
      this.newsItems = this._resourcesToNewsItems(this.edResources) || [];
      this.loading = false;
    });
  }

  get_image(resource: Resource) {
    if (resource.video_code) {
      return 'https://img.youtube.com/vi/' + resource.video_code + '/hqdefault.jpg';
    } else {
      return '/assets/about/feature.jpg';
    }
  }

  private _resourcesToNewsItems(ed_resources: Resource[]): NewsItem[] {
    if (this.edResources && this.edResources.length > 0) {
      return ed_resources
        .sort((a, b) => (a.id > b.id) ? 1 : -1)
        .map(r => {
          let label: string;
          if (r.video_code) {
            label = 'Watch this video';
          }
          const n: NewsItem = {
            title: r.title,
            description: r.description.substr(0, 100) + '...',
            url: `/${r.type.toLowerCase()}/${r.id}`,
            type: HitType.RESOURCE,
            img: this.get_image(r),
            imgClass: 'center-center',
            label: label
          };
          return n;
        });
    }
  }
}
