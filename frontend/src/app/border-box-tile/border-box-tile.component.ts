import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {TypeIconComponent} from '@app/type-icon/type-icon.component';

@Component({
  standalone: true,
  selector: 'app-border-box-tile',
  templateUrl: './border-box-tile.component.html',
  styleUrls: ['./border-box-tile.component.scss'],
  imports: [DetailsLinkComponent, CommonModule, TypeIconComponent],
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
