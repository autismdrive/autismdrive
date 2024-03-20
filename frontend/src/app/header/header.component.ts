import {animate, state, style, transition, trigger} from '@angular/animations';
import {MediaMatcher} from '@angular/cdk/layout';
import {AfterViewInit, ChangeDetectorRef, Component, Input, OnDestroy} from '@angular/core';
import {Router} from '@angular/router';
import {fromEvent} from 'rxjs';
import {filter, map, pairwise, share, throttleTime} from 'rxjs/operators';
import {Direction, HeaderState, MenuState, ViewportWidth} from '../_models/scroll';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {ConfigService} from '../_services/config/config.service';

const boxShadow = '0px 5px 5px 0px rgba(0, 0, 0, 0.3)';
const stateHiddenCollapsed = MenuState.Hidden + '-' + HeaderState.Collapsed;
const stateHiddenExpanded = MenuState.Hidden + '-' + HeaderState.Expanded;
const stateVisibleCollapsed = MenuState.Visible + '-' + HeaderState.Collapsed;
const stateVisibleExpanded = MenuState.Visible + '-' + HeaderState.Expanded;
const easing = '500ms ease-in-out';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  animations: [
    trigger('toggleMobileMenu', [
      state(stateHiddenCollapsed + '-' + ViewportWidth.Small, style({top: '-100vh'})),
      state(stateHiddenExpanded + '-' + ViewportWidth.Small, style({top: '-100vh'})),
      state(stateVisibleCollapsed + '-' + ViewportWidth.Small, style({top: '64px', 'box-shadow': boxShadow})),
      state(stateVisibleExpanded + '-' + ViewportWidth.Small, style({top: '64px', 'box-shadow': boxShadow})),
      transition('* => *', animate(easing)),
    ]),
    trigger('toggleUvaHeader', [
      state(HeaderState.Collapsed, style({top: '-40px', height: '40px'})),
      state(HeaderState.Expanded, style({top: '0px', height: '40px'})),
      transition('* => *', animate(easing)),
    ]),
    trigger('toggleMenuBar', [
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Small,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(stateHiddenExpanded + '-' + ViewportWidth.Small, style({top: '0px', height: '64px', 'box-shadow': 'none'})),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Small,
        style({top: '0px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Small,
        style({top: '0px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Medium,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Medium,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Medium,
        style({top: '0px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Medium,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Large,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Large,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Large,
        style({top: '0px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Large,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      transition('* => *', animate(easing)),
    ]),
    trigger('toggleTaglineToolbar', [
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Small,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Small,
        style({top: '104px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Medium,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Medium,
        style({top: '104px', height: '40px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Large,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Large,
        style({top: '104px', height: '40px', 'box-shadow': boxShadow}),
      ),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Small,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Small,
        style({top: '104px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Medium,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Medium,
        style({top: '104px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleCollapsed + '-' + ViewportWidth.Large,
        style({top: '0px', height: '40px', 'box-shadow': 'none'}),
      ),
      state(
        stateVisibleExpanded + '-' + ViewportWidth.Large,
        style({top: '104px', height: '40px', 'box-shadow': 'none'}),
      ),
      transition('* => *', animate(easing)),
    ]),
    trigger('toggleBackground', [
      state(HeaderState.Collapsed + '-' + ViewportWidth.Small, style({top: '0px', height: '64px'})),
      state(HeaderState.Expanded + '-' + ViewportWidth.Small, style({top: '0px', height: '64px'})),
      state(HeaderState.Collapsed + '-' + ViewportWidth.Medium, style({top: '0px', height: '64px'})),
      state(HeaderState.Expanded + '-' + ViewportWidth.Medium, style({top: '0px', height: '144px'})),
      state(HeaderState.Collapsed + '-' + ViewportWidth.Large, style({top: '0px', height: '64px'})),
      state(HeaderState.Expanded + '-' + ViewportWidth.Large, style({top: '0px', height: '144px'})),
      transition('* => *', animate(easing)),
    ]),
    trigger('toggleResourceBar', [
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Small,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(stateHiddenExpanded + '-' + ViewportWidth.Small, style({top: '0px', height: '64px', 'box-shadow': 'none'})),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Medium,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Medium,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      state(
        stateHiddenCollapsed + '-' + ViewportWidth.Large,
        style({top: '0px', height: '64px', 'box-shadow': boxShadow}),
      ),
      state(
        stateHiddenExpanded + '-' + ViewportWidth.Large,
        style({top: '40px', height: '64px', 'box-shadow': 'none'}),
      ),
      transition('* => *', animate(easing)),
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

  private _mobileQueryListener: () => void;
  private _mdMediaQueryListener: () => void;
  private _lgMediaQueryListener: () => void;

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

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private authenticationService: AuthenticationService,
    private router: Router,
    private api: ApiService,
    public config: ConfigService,
    media: MediaMatcher,
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
