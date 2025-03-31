import {NgForOf} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect, signal, WritableSignal} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {Router, RouterModule} from '@angular/router';
import {BorderBoxTileComponent} from '@app/border-box-tile/border-box-tile.component';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {NewsItemComponent} from '@app/news-item/news-item.component';
import {HitType} from '@models/hit_type';
import {NewsItem} from '@models/news-item';
import {Study} from '@models/study';
import {DefaultShowHideDirective, FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {ConfigService} from '@services/config/config.service';
import {lastValueFrom} from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  imports: [
    BorderBoxTileComponent,
    DetailsLinkComponent,
    NewsItemComponent,
    NgForOf,
    FlexModule,
    RouterModule,
    DefaultShowHideDirective,
  ],
  providers: [ConfigService],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent {
  currentStudies: WritableSignal<Study[]> = signal(undefined);
  newsItems: WritableSignal<NewsItem[]> = signal(undefined);

  constructor(
    private api: ApiService,
    private router: Router,
    private configService: ConfigService,
    private meta: Meta,
  ) {
    effect(() => {
      if (this.configService.props()) {
        this.loadStudies();

        if (this.configService.mirroring) {
          this.router.navigate(['mirrored']);
        }

        this.updateTags();
      }
    })
  }

  private _studiesToNewsItems(studies: Study[]): NewsItem[] {
    if (this.currentStudies && this.currentStudies.length > 0) {
      return studies.map(s => {
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

  private async loadStudies() {
    const studies = await lastValueFrom(this.api.getStudiesByStatus('currently_enrolling'));
    this.currentStudies.set(studies);
    this.newsItems.set(this._studiesToNewsItems(studies));
  }

  private updateTags() {
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
}
