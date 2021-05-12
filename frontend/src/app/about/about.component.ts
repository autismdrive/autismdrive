import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {

  constructor(
    private router: Router,
    private meta: Meta,
  ) {
    this.meta.updateTag(
      { property: 'og:image', content: location.origin + '/assets/about/diversity.jpg' },
      `property='og:image'`);
    this.meta.updateTag(
      { property: 'og:image:secure_url', content: location.origin + '/assets/about/diversity.jpg' },
      `property='og:image:secure_url'`);
    this.meta.updateTag(
      { name: 'twitter:image', content: location.origin + '/assets/about/diversity.jpg' },
      `name='twitter:image'`);
  }

  ngOnInit() {
  }

  goRegister($event) {
    $event.preventDefault();
    this.router.navigate(['register']);
  }
}
