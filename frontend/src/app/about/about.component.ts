import {Component} from '@angular/core';
import {MatButton, MatButtonModule} from '@angular/material/button';
import {Meta} from '@angular/platform-browser';
import {Router} from '@angular/router';
import {DefaultLayoutDirective, DefaultShowHideDirective, ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';

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
  ) {
    this.meta.updateTag(
      {property: 'og:image', content: location.origin + '/public/about/diversity.jpg'},
      `property='og:image'`,
    );
    this.meta.updateTag(
      {property: 'og:image:secure_url', content: location.origin + '/public/about/diversity.jpg'},
      `property='og:image:secure_url'`,
    );
    this.meta.updateTag(
      {name: 'twitter:image', content: location.origin + '/public/about/diversity.jpg'},
      `name='twitter:image'`,
    );
  }

  goRegister($event) {
    $event.preventDefault();
    this.router.navigate(['register']);
  }
}
