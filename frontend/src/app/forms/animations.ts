import {
  animate,
  animateChild,
  group,
  query,
  sequence,
  style,
  transition,
  trigger,
  AnimationTriggerMetadata,
  state
} from '@angular/animations';

const easing = '0.5s ease-in-out';
const hide = style({ opacity: 0 });
const show = style({ opacity: 1 });
const transitionOut = [show, animate(easing, hide)];
const transitionIn = [hide, animate(easing, show)];
const optional = { optional: true };
const normal = style({ opacity: 1, transform: 'translateX(0%) scale(1)' });
const zoomedOut = style({ opacity: 0, transform: 'translateX(0%) scale(0)' });
const zoomedIn = style({ opacity: 0, transform: 'translateX(0%) scale(10)' });
const offScreenLeft = style({ opacity: 0, transform: 'translateX(-100%) scale(1)' });
const offScreenRight = style({ opacity: 0, transform: 'translateX(100%) scale(1)' });
const fadedOut = style({ opacity: 0, transform: 'translateX(0%) scale(1)' });

export function fadeTransition(): AnimationTriggerMetadata {
  return trigger('fadeTransition', [
    transition('* <=> *', [
      query(':enter, :leave', show, optional),
      query(':enter', hide, optional),
      sequence([
        query(':leave', animateChild(), optional),
        group([
          query(':leave', transitionOut, optional),
          query(':enter', transitionIn, optional),
        ]),
        query(':enter', animateChild(), optional),
      ])
    ])
  ]);
}

export function slideTransition(): AnimationTriggerMetadata {
  return trigger('slideTransition', [
    transition('* <=> *', [
      query(':enter, :leave',
        style({ position: 'fixed', width: '100%' }), optional),
      group([
        query(':enter', [
          style({ transform: 'translateX(100%)' }),
          animate(easing, style({ transform: 'translateX(0%)' }))
        ], optional),
        query(':leave', [
          style({ transform: 'translateX(0%)' }),
          animate(easing, style({ transform: 'translateX(-100%)' }))
        ], optional),
      ])
    ])
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
    transition('* => void', [
      animate(easing, hide)
    ]),
    transition('* => delay-fade-enter', [
      fadedOut,
      animate('1.5s ease-in-out', fadedOut),
      animate(easing, normal)
    ]),
    transition('* => delay-fade-exit', [
      normal,
      animate('1.5s ease-in-out', normal),
      animate(easing, fadedOut)
    ]),
    transition('* => fade-enter', [
      fadedOut,
      animate(easing, fadedOut),
      animate(easing, normal)
    ]),
    transition('* => fade-exit', [
      normal,
      animate(easing, normal),
      animate(easing, fadedOut)
    ]),
    transition('* => zoom-in-enter', [
      zoomedOut,
      animate(easing, zoomedOut),
      animate(easing, normal)
    ]),
    transition('* => zoom-in-exit', [
      normal,
      animate(easing, zoomedIn),
      animate(easing, zoomedIn)
    ]),
    transition('* => zoom-out-enter', [
      zoomedIn,
      animate(easing, zoomedIn),
      animate(easing, normal)
    ]),
    transition('* => zoom-out-exit', [
      normal,
      animate(easing, zoomedOut),
      animate(easing, zoomedOut)
    ]),
    transition('* => slide-left-enter', [
      offScreenRight,
      animate(easing, offScreenRight),
      animate(easing, normal)
    ]),
    transition('* => slide-left-exit', [
      normal,
      animate(easing, offScreenLeft),
      animate(easing, offScreenLeft)
    ]),
    transition('* => slide-right-enter', [
      offScreenLeft,
      animate(easing, offScreenLeft),
      animate(easing, normal)
    ]),
    transition('* => slide-right-exit', [
      normal,
      animate(easing, offScreenRight),
      animate(easing, offScreenRight)
    ]),
  ]);
}
