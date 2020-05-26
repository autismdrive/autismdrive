import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {NewsItem} from '../_models/news-item';
import {HitType} from '../_models/hit_type';
import {ConfigService} from '../_services/config.service';
import {Meta} from '@angular/platform-browser';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  currentStudies: Study[];
  newsItems: NewsItem[];

  constructor(
    private api: ApiService,
    private router: Router,
    private configService: ConfigService,
    private meta: Meta,
  ) {
    this.api.getStudies().subscribe(all => {
      this.currentStudies = all.filter(s => s.status === 'currently_enrolling');
      this.newsItems = this._studiesToNewsItems(this.currentStudies);
    });
    if (this.configService.mirroring) {
      router.navigate(['mirrored']);
    }
    this.meta.updateTag(
        { property: 'og:image', content: location.origin + '/assets/home/hero-family.jpg' },
        `property='og:image'`);
    this.meta.updateTag(
      { property: 'og:image:secure_url', content: location.origin + '/assets/home/hero-family.jpg' },
      `property='og:image:secure_url'`);
    this.meta.updateTag(
      { name: 'twitter:image', content: location.origin + '/assets/home/hero-family.jpg' },
      `name='twitter:image'`);
  }

  ngOnInit() {
  }

  private _studiesToNewsItems(studies: Study[]): NewsItem[] {
    if (this.currentStudies && this.currentStudies.length > 0) {
      return studies
        .sort((a, b) => (a.id < b.id) ? 1 : -1)
        .map((s, i) => {
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
