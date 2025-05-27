import {
  animate,
  animateChild,
  AnimationTriggerMetadata,
  group,
  query,
  sequence,
  style,
  transition,
  trigger,
} from '@angular/animations';

export const easing = '0.5s ease-in-out';
export const hide = style({opacity: 0});
export const show = style({opacity: 1});
export const transitionOut = [show, animate(easing, hide)];
export const transitionIn = [hide, animate(easing, show)];
export const optional = {optional: true};
export const normal = style({opacity: 1, transform: 'translateX(0%) scale(1)'});

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
