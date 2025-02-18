import {NgClass, NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';

@Component({
  standalone: true,
  selector: 'app-border-box-tile',
  templateUrl: './border-box-tile.component.html',
  styleUrls: ['./border-box-tile.component.scss'],
  imports: [DetailsLinkComponent, NgClass, NgIf],
})
export class BorderBoxTileComponent {
  @Input() iconType: string;
  @Input() isSelected: boolean;
  @Input() url: string;
  @Input() iconSize = 1;
  @Input() title: string;
  @Input() subtitle: string;
  @Input() linkLabel: string;
  @Input() linkSize = 1;
  hover = false;

  constructor() {}
}
