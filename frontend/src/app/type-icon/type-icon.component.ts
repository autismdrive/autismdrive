import { Component, OnInit, Input } from '@angular/core';
import { HitType } from '../_models/query';

@Component({
  selector: 'app-type-icon',
  templateUrl: './type-icon.component.html',
  styleUrls: ['./type-icon.component.scss']
})
export class TypeIconComponent implements OnInit {
  @Input() iconType: string;
  @Input() size: number;

  iconTypes: string[] = Object.values(HitType);

  constructor() { }

  ngOnInit() {
  }

  is(actual: string, expected: string) {
    return HitType[expected.toUpperCase()].toLowerCase() === actual.toLowerCase();
  }

}
