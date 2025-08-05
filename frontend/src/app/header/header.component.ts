import {animate, state, style, transition, trigger} from '@angular/animations';
import {BreakpointObserver} from '@angular/cdk/layout';
import {CommonModule, Location} from '@angular/common';
import {AfterViewInit, ChangeDetectionStrategy, Component, effect, Input, signal, WritableSignal} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {ActivatedRoute, Router, RouterModule} from '@angular/router';
import {LogoComponent} from '@app/logo/logo.component';
import {Direction, HeaderState, MenuState, ViewportWidth} from '@models/scroll';
import {User} from '@models/user';
import {ExtendedModule, FlexModule} from '@ngbracket/ngx-layout';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';
import {WindowService} from '@services/window/window.service';
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
export class HeaderComponent implements AfterViewInit {
  @Input() currentUser: User;
  headerExpanded: WritableSignal<boolean> = signal(true);
  headerExpandedState: WritableSignal<HeaderState> = signal(undefined);
  headerViewportState: WritableSignal<string> = signal(undefined);
  isLg: WritableSignal<boolean> = signal(undefined);
  isMd: WritableSignal<boolean> = signal(undefined);
  isMobile: WritableSignal<boolean> = signal(undefined);
  menuState: WritableSignal<string> = signal(undefined);
  menuVisible: WritableSignal<boolean> = signal(false);
  menuVisibleState: WritableSignal<MenuState> = signal(undefined);
  taglineToolbarState: WritableSignal<string> = signal(undefined);
  resourceToolbarState: WritableSignal<string> = signal(undefined);

  get viewportWidth(): string {
    if (this.isMobile()) {
      return ViewportWidth.Small;
    }
    if (this.isMd()) {
      return ViewportWidth.Medium;
    }
    if (this.isLg()) {
      return ViewportWidth.Large;
    }

    return ViewportWidth.Medium;
  }

  get mirroring(): boolean {
    return this.appEnvironmentService.mirroring;
  }

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private appEnvironmentService: AppEnvironmentService,
    private breakpointObserver: BreakpointObserver,
    private windowService: WindowService,
    private location: Location,
  ) {
    breakpointObserver.observe('(max-width: 959px)').subscribe(s => this.isMobile.set(s.matches));
    breakpointObserver.observe('(min-width: 960px) and (max-width: 1279px)').subscribe(s => this.isMd.set(s.matches));
    breakpointObserver.observe('(min-width: 1280px)').subscribe(s => this.isLg.set(s.matches));

    effect(() => {
      this.headerExpandedState.set(this.headerExpanded() ? HeaderState.Expanded : HeaderState.Collapsed);
    });

    effect(() => {
      this.menuVisibleState.set(this.menuVisible() ? MenuState.Visible : MenuState.Hidden);
    });

    effect(() => {
      this.headerViewportState.set(`${this.headerExpandedState()}-${this.viewportWidth}`);

      const combinedState = `${this.menuVisibleState()}-${this.headerExpandedState()}-${this.viewportWidth}`;
      this.menuState.set(combinedState);
      this.taglineToolbarState.set(combinedState);
      this.resourceToolbarState.set(`${MenuState.Hidden}-${this.headerExpandedState()}-${this.viewportWidth}`);
    });
  }

  // https://gist.github.com/zetsnotdead/08cc5632f3427d41254068d322807c51
  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  goLogin() {
    const onLoginScreen = /^\/login/.test(this.location.path());
    const onLogoutScreen = /^\/logout/.test(this.location.path());
    const onHomeScreen = /^\/home/.test(this.location.path());
    const onTimedOutScreen = /^\/timedout/.test(this.location.path());
    if (onHomeScreen || onLoginScreen || onLogoutScreen || onTimedOutScreen) {
      this.router.navigate(['/login']);
    } else {
      this.router.navigate(['/login'], {queryParams: {returnUrl: this.location.path()}});
    }
  }

  toggleMenu() {
    this.menuVisible.set(!this.menuVisible());
  }

  onHomeScreen() {
    return /^\/home/.test(this.location.path());
  }

  onResourceScreen() {
    return /^\/search/.test(this.location.path());
  }

  watchScrollEvents() {
    const scroll$ = fromEvent(this.windowService.window, 'scroll').pipe(
      throttleTime(10),
      map((_: Event) => this.windowService.window.pageYOffset),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      share(),
    );

    scroll$.pipe(filter(direction => direction === Direction.Up)).subscribe(() => {
      this.headerExpanded.set(true);
    });

    scroll$.pipe(filter(direction => direction === Direction.Down)).subscribe(() => {
      this.menuVisible.set(false);
      this.headerExpanded.set(false);
    });
  }
}
