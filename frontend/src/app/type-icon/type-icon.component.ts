import { Component, OnInit, Input } from '@angular/core';
import {HitType} from '../_models/hit_type';

@Component({
  selector: 'app-type-icon',
  templateUrl: './type-icon.component.html',
  styleUrls: ['./type-icon.component.scss']
})
export class TypeIconComponent implements OnInit {
  @Input() iconType: string;
  @Input() size: number;

  iconTypes: string[] = HitType.all().map(ht => ht.name);

  constructor() { }

  ngOnInit() {
  }

  is(actual: string, expected: string) {
    return actual === expected;
  }

  get pxSize() {
    return `${this.size * 16}px`;
  }

}
