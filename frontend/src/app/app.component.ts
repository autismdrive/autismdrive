import {DOCUMENT} from '@angular/common';
import {HttpClient} from '@angular/common/http';
import {ChangeDetectionStrategy, Component, effect, Inject, OnInit, Renderer2} from '@angular/core';
import {Meta} from '@angular/platform-browser';
import {ActivatedRoute, ActivationEnd, ActivationStart, NavigationEnd, Router, RouterOutlet} from '@angular/router';
import {FooterComponent} from '@app/footer/footer.component';
import {HeaderComponent} from '@app/header/header.component';
import {User} from '@models/user';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  imports: [HeaderComponent, FooterComponent, RouterOutlet],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent implements OnInit {
  title = 'Autism DRIVE';
  hideHeader = false;

  public constructor(
    private authenticationService: AuthenticationService,
    private router: Router,
    private meta: Meta,
    private route: ActivatedRoute,
    private appEnvironmentService: AppEnvironmentService,
  ) {
    effect(() => {
      if (this.appEnvironmentService.props()) {
        this.router.events.subscribe(e => {
          if (e instanceof ActivationStart || e instanceof ActivationEnd) {
            if (e.snapshot && e.snapshot.data) {
              const data = e.snapshot.data;
              this.hideHeader = !!data['hideHeader'];
            }
          }
        });
        this.meta.addTags([
          {property: 'og:url', content: location.origin},
          {property: 'og:image', content: location.origin + '/assets/home/hero-family.jpg'},
          {property: 'og:image:secure_url', content: location.origin + '/assets/home/hero-family.jpg'},
          {name: 'twitter:image', content: location.origin + '/assets/home/hero-family.jpg'},
        ]);
      }
    });
  }

  ngOnInit() {
    console.log('AppComponent > ngOnInit');
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const title = this.route.snapshot.firstChild.data['title'];
        const bodyElement = document.querySelector('body');
        bodyElement.classList.toggle('is-home', this.router.url === '/home');
        if (title) {
          this.meta.updateTag({property: 'og:title', content: title}, `property='og:title'`);
          this.meta.updateTag({name: 'twitter:text:title', content: title}, `name='twitter:text:title'`);
        }
        this.meta.updateTag({property: 'og:url', content: location.href}, `property='og:url'`);
      }
    });
  }

  get currentUser(): User {
    return this.authenticationService.currentUser();
  }
}
