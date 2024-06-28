import {Component} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {Router} from '@angular/router';
import {HitType} from '../_models/hit_type';
import {NewsItem} from '../_models/news-item';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {ConfigService} from '../_services/config/config.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  currentStudies: Study[];
  newsItems: NewsItem[];

  constructor(
    private api: ApiService,
    private router: Router,
    private configService: ConfigService,
    private meta: Meta,
  ) {
    this.api.getStudiesByStatus('currently_enrolling').subscribe(studies => {
      this.currentStudies = studies;
      this.newsItems = this._studiesToNewsItems(studies);
    });
    if (this.configService.mirroring) {
      router.navigate(['mirrored']);
    }
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/assets/home/hero-family.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/assets/home/hero-family.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/assets/home/hero-family.jpg'},
      `name='twitter:image'`,
    );
  }

  private _studiesToNewsItems(studies: Study[]): NewsItem[] {
    if (this.currentStudies && this.currentStudies.length > 0) {
      return studies.map((s, i) => {
        const n: NewsItem = {
          title: s.short_title || s.title,
          description: s.short_description || s.description,
          url: `/study/${s.id}`,
          type: HitType.STUDY,
          img: s.image_url,
          imgClass: 'center-center',
        };

        return n;
      });
    }
  }
}
