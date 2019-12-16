import { Component, OnInit } from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';
import {User} from '../_models/user';
import {Resource} from '../_models/resource';
import {NewsItem} from '../_models/news-item';
import {HitType} from '../_models/hit_type';
import {Hit} from '../_models/query';

@Component({
  selector: 'app-uva-education',
  templateUrl: './uva-education.component.html',
  styleUrls: ['./uva-education.component.scss']
})
export class UvaEducationComponent implements OnInit {
  edResources: Resource[];
  newsItems: NewsItem[];
  currentUser: User;

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
    this.api.getResources().subscribe( resources => {
      this.edResources = resources;
      this.newsItems = this._resourcesToNewsItems(this.edResources);
    })
  }


  private _resourcesToNewsItems(ed_resources: Resource[]): NewsItem[] {
    if (this.edResources && this.edResources.length > 0) {
      return ed_resources
        .sort((a, b) => (a.id > b.id) ? 1 : -1)
        .map((r, i) => {
          const n: NewsItem = {
            title: r.title,
            description: r.description.substr(0, 100) + '...',
            url: `/${r.type.toLowerCase()}/${r.id}`,
            type: HitType.RESOURCE,
            img: 'https://img.youtube.com/vi/' + r.video_code +'/hqdefault.jpg',
            imgClass: 'center-center',
          };
          return n;
        });
    }
  }

}
