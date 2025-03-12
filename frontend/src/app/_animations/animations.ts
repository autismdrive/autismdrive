import {
  animate,
  animateChild,
  AnimationTriggerMetadata,
  group,
  query,
  sequence,
  state,
  style,
  transition,
  trigger,
} from '@angular/animations';
import {HeaderState, MenuState, ViewportWidth} from '@models/scroll';

const easing = '0.5s ease-in-out';
const hide = style({opacity: 0});
const show = style({opacity: 1});
const transitionOut = [show, animate(easing, hide)];
const transitionIn = [hide, animate(easing, show)];
const optional = {optional: true};
const normal = style({opacity: 1, transform: 'translateX(0%) scale(1)'});
const zoomedOut = style({opacity: 0, transform: 'translateX(0%) scale(0)'});
const zoomedIn = style({opacity: 0, transform: 'translateX(0%) scale(10)'});
const offScreenLeft = style({opacity: 0, transform: 'translateX(-100%) scale(1)'});
const offScreenRight = style({opacity: 0, transform: 'translateX(100%) scale(1)'});
const fadedOut = style({opacity: 0, transform: 'translateX(0%) scale(1)'});
const stateHiddenCollapsed = MenuState.Hidden + '-' + HeaderState.Collapsed;
const stateHiddenExpanded = MenuState.Hidden + '-' + HeaderState.Expanded;
const stateVisibleCollapsed = MenuState.Visible + '-' + HeaderState.Collapsed;
const stateVisibleExpanded = MenuState.Visible + '-' + HeaderState.Expanded;
const boxShadow = '0px 5px 5px 0px rgba(0, 0, 0, 0.3)';

export function fadeTransition(): AnimationTriggerMetadata {
  return trigger('fadeTransition', [
    transition('* <=> *', [
      query(':enter, :leave', show, optional),
      query(':enter', hide, optional),
      sequence([
        query(':leave', animateChild(), optional),
        group([query(':leave', transitionOut, optional), query(':enter', transitionIn, optional)]),
        query(':enter', animateChild(), optional),
      ]),
    ]),
  ]);
}

export function slideTransition(): AnimationTriggerMetadata {
  return trigger('slideTransition', [
    transition('* <=> *', [
      query(':enter, :leave', style({position: 'fixed', width: '100%'}), optional),
      group([
        query(
          ':enter',
          [style({transform: 'translateX(100%)'}), animate(easing, style({transform: 'translateX(0%)'}))],
          optional,
        ),
        query(
          ':leave',
          [style({transform: 'translateX(0%)'}), animate(easing, style({transform: 'translateX(-100%)'}))],
          optional,
        ),
      ]),
    ]),
  ]);
}

export function zoomTransition(): AnimationTriggerMetadata {
  return trigger('zoomTransition', [
    state('delay-fade-enter', normal),
    state('delay-fade-exit', normal),
    state('fade-enter', normal),
    state('fade-exit', normal),
    state('zoom-in-enter', normal),
    state('zoom-in-exit', normal),
    state('zoom-out-enter', normal),
    state('zoom-out-exit', normal),
    state('slide-right-enter', normal),
    state('slide-right-exit', normal),
    state('slide-left-enter', normal),
    state('slide-left-exit', normal),
    transition('* => void', [animate(easing, hide)]),
    transition('* => delay-fade-enter', [fadedOut, animate('1.5s ease-in-out', fadedOut), animate(easing, normal)]),
    transition('* => delay-fade-exit', [normal, animate('1.5s ease-in-out', normal), animate(easing, fadedOut)]),
    transition('* => fade-enter', [fadedOut, animate(easing, fadedOut), animate(easing, normal)]),
    transition('* => fade-exit', [normal, animate(easing, normal), animate(easing, fadedOut)]),
    transition('* => zoom-in-enter', [zoomedOut, animate(easing, zoomedOut), animate(easing, normal)]),
    transition('* => zoom-in-exit', [normal, animate(easing, zoomedIn), animate(easing, zoomedIn)]),
    transition('* => zoom-out-enter', [zoomedIn, animate(easing, zoomedIn), animate(easing, normal)]),
    transition('* => zoom-out-exit', [normal, animate(easing, zoomedOut), animate(easing, zoomedOut)]),
    transition('* => slide-left-enter', [offScreenRight, animate(easing, offScreenRight), animate(easing, normal)]),
    transition('* => slide-left-exit', [normal, animate(easing, offScreenLeft), animate(easing, offScreenLeft)]),
    transition('* => slide-right-enter', [offScreenLeft, animate(easing, offScreenLeft), animate(easing, normal)]),
    transition('* => slide-right-exit', [normal, animate(easing, offScreenRight), animate(easing, offScreenRight)]),
  ]);
}

export const commonAnimations = [
  trigger('toggleMobileMenu', [
    state(stateHiddenCollapsed + '-' + ViewportWidth.Small, style({top: '-100vh'})),
    state(stateHiddenExpanded + '-' + ViewportWidth.Small, style({top: '-100vh'})),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Small,
      style({
        top: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    transition('* => *', animate(easing)),
  ]),
  trigger('toggleUvaHeader', [
    state(
      HeaderState.Collapsed,
      style({
        top: '-40px',
        height: '40px',
      }),
    ),
    state(HeaderState.Expanded, style({top: '0px', height: '40px'})),
    transition('* => *', animate(easing)),
  ]),
  trigger('toggleMenuBar', [
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Medium,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Medium,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Large,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Large,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    transition('* => *', animate(easing)),
  ]),
  trigger('toggleTaglineToolbar', [
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Small,
      style({
        top: '104px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Medium,
      style({
        top: '104px',
        height: '40px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Large,
      style({
        top: '104px',
        height: '40px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Small,
      style({
        top: '104px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Medium,
      style({
        top: '104px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleCollapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateVisibleExpanded + '-' + ViewportWidth.Large,
      style({
        top: '104px',
        height: '40px',
        'box-shadow': 'none',
      }),
    ),
    transition('* => *', animate(easing)),
  ]),
  trigger('toggleBackground', [
    state(
      HeaderState.Collapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
      }),
    ),
    state(
      HeaderState.Expanded + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
      }),
    ),
    state(
      HeaderState.Collapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '64px',
      }),
    ),
    state(
      HeaderState.Expanded + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '144px',
      }),
    ),
    state(
      HeaderState.Collapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '64px',
      }),
    ),
    state(
      HeaderState.Expanded + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '144px',
      }),
    ),
    transition('* => *', animate(easing)),
  ]),
  trigger('toggleResourceBar', [
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Small,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Medium,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Medium,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    state(
      stateHiddenCollapsed + '-' + ViewportWidth.Large,
      style({
        top: '0px',
        height: '64px',
        'box-shadow': boxShadow,
      }),
    ),
    state(
      stateHiddenExpanded + '-' + ViewportWidth.Large,
      style({
        top: '40px',
        height: '64px',
        'box-shadow': 'none',
      }),
    ),
    transition('* => *', animate(easing)),
  ]),
];
