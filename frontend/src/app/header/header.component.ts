import {animate, state, style, transition, trigger} from '@angular/animations';
import {MediaMatcher} from '@angular/cdk/layout';
import {CommonModule} from '@angular/common';
import {AfterViewInit, ChangeDetectionStrategy, ChangeDetectorRef, Component, Input, OnDestroy} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {provideAnimations} from '@angular/platform-browser/animations';
import {Router, RouterModule} from '@angular/router';
import {LogoComponent} from '@app/logo/logo.component';
import {Direction, HeaderState, MenuState, ViewportWidth} from '@models/scroll';
import {User} from '@models/user';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {fromEvent} from 'rxjs';
import {filter, map, pairwise, share, throttleTime} from 'rxjs/operators';

@Component({
  standalone: true,
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  imports: [
    CommonModule,
    ExtendedModule,
    FlexModule,
    LogoComponent,
    MatButtonModule,
    MatIconModule,
    MatToolbarModule,
    RouterModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  animations: [
    trigger('toggleMobileMenu', [
      state('hidden-collapsed-sm', style({top: '-100vh'})),
      state('hidden-expanded-sm', style({top: '-100vh'})),
      state(
        'visible-collapsed-sm',
        style({
          top: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'visible-expanded-sm',
        style({
          top: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
    trigger('toggleUvaHeader', [
      state(
        'collapsed',
        style({
          top: '-40px',
          height: '40px',
        }),
      ),
      state('expanded', style({top: '0px', height: '40px'})),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
    trigger('toggleMenuBar', [
      state(
        'hidden-collapsed-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-collapsed-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-collapsed-md',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-md',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-collapsed-md',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-md',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-collapsed-lg',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-lg',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-collapsed-lg',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-lg',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
    trigger('toggleTaglineToolbar', [
      state(
        'hidden-collapsed-sm',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-expanded-sm',
        style({
          top: '104px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-collapsed-md',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-expanded-md',
        style({
          top: '104px',
          height: '40px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-collapsed-lg',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-expanded-lg',
        style({
          top: '104px',
          height: '40px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'visible-collapsed-sm',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-sm',
        style({
          top: '104px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-collapsed-md',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-md',
        style({
          top: '104px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-collapsed-lg',
        style({
          top: '0px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'visible-expanded-lg',
        style({
          top: '104px',
          height: '40px',
          'box-shadow': 'none',
        }),
      ),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
    trigger('toggleBackground', [
      state(
        'collapsed-sm',
        style({
          top: '0px',
          height: '64px',
        }),
      ),
      state(
        'expanded-sm',
        style({
          top: '0px',
          height: '64px',
        }),
      ),
      state(
        'collapsed-md',
        style({
          top: '0px',
          height: '64px',
        }),
      ),
      state(
        'expanded-md',
        style({
          top: '0px',
          height: '144px',
        }),
      ),
      state(
        'collapsed-lg',
        style({
          top: '0px',
          height: '64px',
        }),
      ),
      state(
        'expanded-lg',
        style({
          top: '0px',
          height: '144px',
        }),
      ),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
    trigger('toggleResourceBar', [
      state(
        'hidden-collapsed-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-sm',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-collapsed-md',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-md',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      state(
        'hidden-collapsed-lg',
        style({
          top: '0px',
          height: '64px',
          'box-shadow': '0px 5px 5px 0px rgba(0, 0, 0, 0.3)',
        }),
      ),
      state(
        'hidden-expanded-lg',
        style({
          top: '40px',
          height: '64px',
          'box-shadow': 'none',
        }),
      ),
      transition('* => *', animate('0.5s ease-in-out')),
    ]),
  ],
})
export class HeaderComponent implements AfterViewInit, OnDestroy {
  private headerExpanded = true;
  @Input() currentUser: User;
  menuVisible = false;
  mobileQuery: MediaQueryList;
  mdMediaQuery: MediaQueryList;
  lgMediaQuery: MediaQueryList;

  private readonly _mobileQueryListener: () => void;
  private readonly _mdMediaQueryListener: () => void;
  private readonly _lgMediaQueryListener: () => void;

  get viewportWidth(): string {
    if (this.mobileQuery.matches) {
      return ViewportWidth.Small;
    }
    if (this.mdMediaQuery.matches) {
      return ViewportWidth.Medium;
    }
    if (this.lgMediaQuery.matches) {
      return ViewportWidth.Large;
    }
  }

  get headerViewportState(): string {
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${headerState}-${this.viewportWidth}`;
  }

  get menuState(): string {
    const menuState = this.menuVisible ? MenuState.Visible : MenuState.Hidden;
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${menuState}-${headerState}-${this.viewportWidth}`;
  }

  get headerExpandedState(): string {
    return this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
  }

  get taglineToolbarState(): string {
    const menuState = this.menuVisible ? MenuState.Visible : MenuState.Hidden;
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${menuState}-${headerState}-${this.viewportWidth}`;
  }

  get resourceToolbarState(): string {
    const menuState = MenuState.Hidden;
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${menuState}-${headerState}-${this.viewportWidth}`;
  }

  get mirroring(): boolean {
    return this.appEnvironmentService.mirroring;
  }

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private router: Router,
    private appEnvironmentService: AppEnvironmentService,
    media: MediaMatcher,
  ) {
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this.mdMediaQuery = media.matchMedia('(min-width: 960px) and (max-width: 1279px)');
    this.lgMediaQuery = media.matchMedia('(min-width: 1280px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this._mdMediaQueryListener = () => changeDetectorRef.detectChanges();
    this._lgMediaQueryListener = () => changeDetectorRef.detectChanges();

    this.mobileQuery.addListener(this._mobileQueryListener);

    this.mdMediaQuery.addListener(this._mdMediaQueryListener);

    this.lgMediaQuery.addListener(this._lgMediaQueryListener);
  }

  // https://gist.github.com/zetsnotdead/08cc5632f3427d41254068d322807c51
  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  ngOnDestroy(): void {
    this.mobileQuery.removeListener(this._mobileQueryListener);

    this.mdMediaQuery.removeListener(this._mdMediaQueryListener);

    this.lgMediaQuery.removeListener(this._lgMediaQueryListener);
  }

  goLogin() {
    const onLoginScreen = /^\/login/.test(this.router.url);
    const onLogoutScreen = /^\/logout/.test(this.router.url);
    const onHomeScreen = /^\/home/.test(this.router.url);
    const onTimedOutScreen = /^\/timedout/.test(this.router.url);
    if (onHomeScreen || onLoginScreen || onLogoutScreen || onTimedOutScreen) {
      this.router.navigate(['/login']);
    } else {
      this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
    }
  }

  toggleMenu() {
    this.menuVisible = !this.menuVisible;
  }

  onHomeScreen() {
    return /^\/home/.test(this.router.url);
  }

  onResourceScreen() {
    return /^\/search/.test(this.router.url);
  }

  watchScrollEvents() {
    const scroll$ = fromEvent(window, 'scroll').pipe(
      throttleTime(10),
      map((e: Event) => window.pageYOffset),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      share(),
    );

    scroll$.pipe(filter(direction => direction === Direction.Up)).subscribe(() => {
      this.headerExpanded = true;
    });

    scroll$.pipe(filter(direction => direction === Direction.Down)).subscribe(() => {
      this.menuVisible = false;
      this.headerExpanded = false;
    });
  }
}
