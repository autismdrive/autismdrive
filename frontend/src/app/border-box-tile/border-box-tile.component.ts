import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-border-box-tile',
  templateUrl: './border-box-tile.component.html',
  styleUrls: ['./border-box-tile.component.scss']
})
export class BorderBoxTileComponent implements OnInit {
  @Input() iconType: string;
  @Input() isSelected: boolean;
  @Input() url: string;
  @Input() iconSize = 1;
  @Input() title: string;
  @Input() subtitle: string;
  @Input() linkLabel: string;
  @Input() linkSize = 1;
  hover = false;

  constructor() { }

  ngOnInit() {
  }
}
