import {isPlatformBrowser} from '@angular/common';
import {Component, Inject, PLATFORM_ID} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {Meta} from '@angular/platform-browser';
import {Router} from '@angular/router';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss'],
  imports: [FlexModule, ExtendedModule, MatButtonModule],
})
export class AboutComponent {
  constructor(
    private router: Router,
    private meta: Meta,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {
    this.meta.updateTag(
      {property: 'og:image', content: this.location.origin + '/public/about/diversity.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: this.location.origin + '/public/about/diversity.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: this.location.origin + '/public/about/diversity.jpg'},
      `name='twitter:image'`,
    );
  }

  get location() {
    if (isPlatformBrowser(this.platformId)) return location;

    // Fallback for server-side rendering
    return {
      origin: 'http://localhost:4200', // Default origin for SSR
      href: 'http://localhost:4200', // Default href for SSR
    };
  }

  goRegister($event) {
    $event.preventDefault();
    this.router.navigate(['register']);
  }
}
