import {Component, Input} from '@angular/core';
import {HitType} from '@models/hit_type';

@Component({
  selector: 'app-type-icon',
  templateUrl: './type-icon.component.html',
  styleUrls: ['./type-icon.component.scss'],
})
export class TypeIconComponent {
  @Input() iconType: string;
  @Input() size: number;

  iconTypes: string[] = HitType.all().map(ht => ht.name);

  constructor() {}

  is(actual: string, expected: string) {
    return actual === expected;
  }

  get pxSize() {
    return `${this.size * 16}px`;
  }
}
