import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { AfterViewInit, Component, HostBinding } from '@angular/core';
import { fromEvent } from 'rxjs';
import {
  distinctUntilChanged,
  filter,
  map,
  pairwise,
  share,
  throttleTime
} from 'rxjs/operators';

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
    trigger('toggle', [
      state(
        VisibilityState.Hidden,
        style({ transform: 'translateY(-100%)', boxShadow: 'none' })
      ),
      state(
        VisibilityState.Visible,
        style({ transform: 'translateY(0)', boxShadow: '0px 10px rgba(0,0,0,0.3)' })
      ),
      transition('* => *', animate('500ms ease-in'))
    ])
  ]
})
export class HeaderComponent implements AfterViewInit {
  private isVisible = true;

  get toggle(): VisibilityState {
    return this.isVisible ? VisibilityState.Visible : VisibilityState.Hidden;
  }

  constructor() { }

  // https://gist.github.com/zetsnotdead/08cc5632f3427d41254068d322807c51
  ngAfterViewInit() {
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

    const scrollDown = scroll$.pipe(
      filter(direction => direction === Direction.Down)
    );

    scrollUp$.subscribe(() => (this.isVisible = true));
    scrollDown.subscribe(() => (this.isVisible = false));
  }
}
