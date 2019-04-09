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
  OnDestroy
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

enum VisibilityState {
  Visible = 'visible',
  Hidden = 'hidden'
}

enum Direction {
  Up = 'Up',
  Down = 'Down'
}

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  animations: [
    trigger('toggleMobileMenu', [
      state(
        VisibilityState.Hidden,
        style({ top: '-100vh' })
      ),
      state(
        VisibilityState.Visible,
        style({ top: '152px' })
      ),
      transition('* => *', animate('500ms ease-in'))
    ]),
    trigger('toggleHide', [
      state(
        VisibilityState.Hidden,
        style({ transform: 'translateY(-200%)' })
      ),
      state(
        VisibilityState.Visible,
        style({ transform: 'translateY(0)' })
      ),
      transition('* => *', animate('500ms ease-in'))
    ]),
    trigger('toggleDock', [
      state(
        VisibilityState.Hidden,
        style({ top: '0px' })
      ),
      state(
        VisibilityState.Visible,
        style({ top: '88px' })
      ),
      transition('* => *', animate('500ms ease-in'))
    ]),
    trigger('toggleBackground', [
      state(
        VisibilityState.Hidden,
        style({ top: '-88px' })
      ),
      state(
        VisibilityState.Visible,
        style({ top: '0px' })
      ),
      transition('* => *', animate('500ms ease-in'))
    ])
  ]
})
export class HeaderComponent implements AfterViewInit, OnDestroy {
  private headerVisible = true;
  @Input() currentUser: User;
  menuVisible = false;
  mobileQuery: MediaQueryList;
  private _mobileQueryListener: () => void;

  get headerState(): VisibilityState {
    return this.headerVisible ? VisibilityState.Visible : VisibilityState.Hidden;
  }

  get menuState(): VisibilityState {
    return this.menuVisible ? VisibilityState.Visible : VisibilityState.Hidden;
  }

  constructor(
    changeDetectorRef: ChangeDetectorRef,
    private authenticationService: AuthenticationService,
    private router: Router,
    media: MediaMatcher,
  ) {
    this.mobileQuery = media.matchMedia('(max-width: 959px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
  }

  // https://gist.github.com/zetsnotdead/08cc5632f3427d41254068d322807c51
  ngAfterViewInit() {
    this.watchScrollEvents();
  }

  ngOnDestroy(): void {
    this.mobileQuery.removeListener(this._mobileQueryListener);
  }

  goLogout($event: MouseEvent) {
    $event.preventDefault();
    this.authenticationService.logout();
    this.router.navigate(['logout']);
  }

  toggleMenu() {
    this.menuVisible = !this.menuVisible;
  }

  watchScrollEvents() {
    const scroll$ = fromEvent(window, 'scroll').pipe(
      throttleTime(10),
      map(() => window.pageYOffset),
      pairwise(),
      map(([y1, y2]): Direction => (y2 < y1 ? Direction.Up : Direction.Down)),
      distinctUntilChanged(),
      share()
    );

    const scrollUp$ = scroll$.pipe(
      filter(direction => direction === Direction.Up)
    );

    const scrollDown$ = scroll$.pipe(
      filter(direction => direction === Direction.Down)
    );

    scrollUp$.subscribe(() => {
      this.headerVisible = true;
    });

    scrollDown$.subscribe(() => {
      this.headerVisible = false;
      this.menuVisible = false;
    });
  }
}
