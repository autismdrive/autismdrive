import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { MediaMatcher } from '@angular/cdk/layout';
import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  Input,
  OnDestroy, OnInit
} from '@angular/core';
import { Router } from '@angular/router';
import { fromEvent } from 'rxjs';
import {
  distinctUntilChanged,
  filter,
  map,
  pairwise,
  share,
  throttleTime
} from 'rxjs/operators';
import { User } from '../_models/user';
import { AuthenticationService } from '../_services/api/authentication-service';
import { ApiService } from '../_services/api/api.service';
import {ConfigService} from '../_services/config.service';

export enum ViewportWidth {
  Small = 'sm',
  Medium = 'md',
  Large = 'lg'
}

export enum MenuState {
  Visible = 'visible',
  Hidden = 'hidden'
}

export enum HeaderState {
  Expanded = 'expanded',
  Collapsed = 'collapsed'
}

export enum Direction {
  Up = 'Up',
  Down = 'Down'
}

const boxShadow = '0px 10px rgba(0, 0, 0, 0.3)';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  animations: [
    trigger('toggleMobileMenu', [
      state(MenuState.Hidden + '-' + HeaderState.Collapsed, style({ top: '-100vh' })),
      state(MenuState.Hidden + '-' + HeaderState.Expanded, style({ top: '-100vh' })),
      state(MenuState.Visible + '-' + HeaderState.Collapsed, style({ top: '64px', 'box-shadow': boxShadow })),
      state(MenuState.Visible + '-' + HeaderState.Expanded, style({ top: '168px', 'box-shadow': boxShadow })),
      transition('* => *', animate('500ms ease-in-out'))
    ]),
    trigger('toggleUvaHeader', [
      state(HeaderState.Collapsed, style({ top: '-40px', height: '40px' })),
      state(HeaderState.Expanded, style({ top: '0px', height: '40px' })),
      transition('* => *', animate('500ms ease-in-out'))
    ]),
    trigger('toggleMenuBar', [
      state(MenuState.Hidden + '-' + HeaderState.Collapsed, style({ top: '0px', height: '64px', 'box-shadow': boxShadow })),
      state(MenuState.Hidden + '-' + HeaderState.Expanded, style({ top: '40px', height: '64px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Collapsed, style({ top: '0px', height: '64px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Expanded, style({ top: '40px', height: '64px', 'box-shadow': 'none' })),
      transition('* => *', animate('500ms ease-in-out'))
    ]),
    trigger('toggleCovid19Toolbar', [
      state(HeaderState.Collapsed, style({ top: '0px', height: '40px' })),
      state(HeaderState.Expanded, style({ top: '104px', height: '40px' })),
      transition('* => *', animate('500ms ease-in-out'))
    ]),
    trigger('toggleTaglineToolbar', [
      state(MenuState.Hidden + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Small, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Hidden + '-' + HeaderState.Expanded + '-' + ViewportWidth.Small, style({ top: '104px', height: '64px', 'box-shadow': boxShadow })),
      state(MenuState.Hidden + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Medium, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Hidden + '-' + HeaderState.Expanded + '-' + ViewportWidth.Medium, style({ top: '144px', height: '40px', 'box-shadow': boxShadow })),
      state(MenuState.Hidden + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Large, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Hidden + '-' + HeaderState.Expanded + '-' + ViewportWidth.Large, style({ top: '144px', height: '40px', 'box-shadow': boxShadow })),
      state(MenuState.Visible + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Small, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Expanded + '-' + ViewportWidth.Small, style({ top: '104px', height: '64px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Medium, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Expanded + '-' + ViewportWidth.Medium, style({ top: '144px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Collapsed + '-' + ViewportWidth.Large, style({ top: '0px', height: '40px', 'box-shadow': 'none' })),
      state(MenuState.Visible + '-' + HeaderState.Expanded + '-' + ViewportWidth.Large, style({ top: '144px', height: '40px', 'box-shadow': 'none' })),
      transition('* => *', animate('500ms ease-in-out'))
    ]),
    trigger('toggleBackground', [
      state(HeaderState.Collapsed, style({ top: '-40px', height: '40px' })),
      state(HeaderState.Expanded, style({ top: '0px', height: '40px' })),
      transition('* => *', animate('500ms ease-in-out'))
    ])
  ]
})
export class HeaderComponent implements AfterViewInit, OnDestroy {
  private headerExpanded = true;
  @Input() currentUser: User;
  menuVisible = false;
  mobileQuery: MediaQueryList;
  mdMediaQuery: MediaQueryList;
  lgMediaQuery: MediaQueryList;

  private _mobileQueryListener: () => void;
  private _mdMediaQueryListener: () => void;
  private _lgMediaQueryListener: () => void;

  get viewportWidth(): string {
    if (this.mobileQuery.matches) { return ViewportWidth.Small; }
    if (this.mdMediaQuery.matches) { return ViewportWidth.Medium; }
    if (this.lgMediaQuery.matches) { return ViewportWidth.Large; }
  }

  get headerState(): string {
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${headerState}-${this.viewportWidth}`;
  }

  get menuState(): string {
    const menuState = this.menuVisible ? MenuState.Visible : MenuState.Hidden;
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${menuState}-${headerState}`;
  }

  get headerExpandedState(): string {
    return this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
  }

  get taglineToolbarState(): string {
    const menuState = this.menuVisible ? MenuState.Visible : MenuState.Hidden;
    const headerState = this.headerExpanded ? HeaderState.Expanded : HeaderState.Collapsed;
    return `${menuState}-${headerState}-${this.viewportWidth}`;
  }

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private authenticationService: AuthenticationService,
    private router: Router,
    private api: ApiService,
    public config: ConfigService,
    media: MediaMatcher
  ) {
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this.mdMediaQuery = media.matchMedia('(min-width: 960px) and (max-width: 1279px)');
    this.lgMediaQuery = media.matchMedia('(min-width: 1280px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this._mdMediaQueryListener = () => changeDetectorRef.detectChanges();
    this._lgMediaQueryListener = () => changeDetectorRef.detectChanges();

    // tslint:disable-next-line:deprecation
    this.mobileQuery.addListener(this._mobileQueryListener);

    // tslint:disable-next-line:deprecation
    this.mdMediaQuery.addListener(this._mdMediaQueryListener);

    // tslint:disable-next-line:deprecation
    this.lgMediaQuery.addListener(this._lgMediaQueryListener);
  }

  // https://gist.github.com/zetsnotdead/08cc5632f3427d41254068d322807c51
  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  ngOnDestroy(): void {
    // tslint:disable-next-line:deprecation
    this.mobileQuery.removeListener(this._mobileQueryListener);

    // tslint:disable-next-line:deprecation
    this.mdMediaQuery.removeListener(this._mdMediaQueryListener);

    // tslint:disable-next-line:deprecation
    this.lgMediaQuery.removeListener(this._lgMediaQueryListener);
  }

  goLogout($event: MouseEvent) {
    $event.preventDefault();
    this.authenticationService.logout();
    this.router.navigate(['logout']);
  }

  goLogin() {
    const onLoginScreen = /^\/login/.test(this.router.url);
    const onLogoutScreen = /^\/logout/.test(this.router.url);
    const onHomeScreen = /^\/home/.test(this.router.url);
    const onTimedOutScreen = /^\/timedout/.test(this.router.url);
    if (onHomeScreen || onLoginScreen || onLogoutScreen || onTimedOutScreen) {
      this.router.navigate(['/login']);
    } else {
      this.router.navigate(['/login'], { queryParams: { returnUrl: this.router.url } });
    }
  }

  toggleMenu() {
    this.menuVisible = !this.menuVisible;
  }

  watchScrollEvents() {
    const scroll$ = fromEvent(window, 'scroll').pipe(
      throttleTime(10),
      map((e: Event) => window.pageYOffset),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      share()
    );

    scroll$
      .pipe(filter(direction => direction === Direction.Up))
      .subscribe(() => {
        this.headerExpanded = true;
      });

    scroll$
      .pipe(filter(direction => direction === Direction.Down))
      .subscribe(() => {
        this.menuVisible = false;
        this.headerExpanded = false;
      });
  }
}
