import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect, signal, WritableSignal} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {Router, RouterModule} from '@angular/router';
import {BorderBoxTileComponent} from '@app/border-box-tile/border-box-tile.component';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {LoadingComponent} from '@app/loading/loading.component';
import {NewsItemComponent} from '@app/news-item/news-item.component';
import {HitType} from '@models/hit_type';
import {NewsItem} from '@models/news-item';
import {Study} from '@models/study';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
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
    CommonModule,
    FlexModule,
    RouterModule,
    ExtendedModule,
    LoadingComponent,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent {
  currentStudies: WritableSignal<Study[]> = signal(undefined);
  newsItems: WritableSignal<NewsItem[]> = signal(undefined);

  constructor(
    private api: ApiService,
    private router: Router,
    private appEnvironmentService: AppEnvironmentService,
    private meta: Meta,
  ) {
    effect(() => {
      if (this.appEnvironmentService.props()) {
        this.loadStudies();

        if (this.appEnvironmentService.mirroring) {
          this.router.navigate(['mirrored']);
        }

        this.updateTags();
      }
    });
  }

  private _studiesToNewsItems(studies: Study[]): NewsItem[] {
    if (this.currentStudies()?.length > 0) {
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

    return [];
  }

  private async loadStudies() {
    const studies = await lastValueFrom(this.api.getStudiesByStatus('currently_enrolling'));
    this.currentStudies.set(studies);
    this.newsItems.set(this._studiesToNewsItems(studies));
  }

  private updateTags() {
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/public/home/hero-family.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/public/home/hero-family.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/public/home/hero-family.jpg'},
      `name='twitter:image'`,
    );
  }
}
