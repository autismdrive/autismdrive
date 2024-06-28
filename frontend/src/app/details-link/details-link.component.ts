import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-details-link',
  templateUrl: './details-link.component.html',
  styleUrls: ['./details-link.component.scss'],
})
export class DetailsLinkComponent {
  @Input() url: string;
  @Input() label = 'Details';
  @Input() size = 1;
  @Input() hover;
  @Input() selected = false;
  @Input() subtitle = '';
  @Input() inverted = false;
  @Input() allCaps = true;
  @Input() externalLink = false;
  shouldHover = false;

  constructor() {}

  onMouseOver() {
    if (this.hover === undefined) {
      this.shouldHover = true;
    }
  }

  onMouseOut() {
    if (this.hover === undefined) {
      this.shouldHover = false;
    }
  }
}
