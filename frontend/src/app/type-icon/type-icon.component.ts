import {CommonModule, NgOptimizedImage} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {HitType} from '@models/hit_type';

@Component({
  standalone: true,
  selector: 'app-type-icon',
  templateUrl: './type-icon.component.html',
  styleUrls: ['./type-icon.component.scss'],
  imports: [CommonModule, MatIconModule, NgOptimizedImage],
})
export class TypeIconComponent {
  @Input() iconType: string;
  @Input() size?: number = 1.5;

  constructor() {}

  get hitType(): HitType {
    const key = this.iconType.toUpperCase();

    if (!(key in HitType)) {
      console.error(`Invalid HitType: ${this.iconType}`);
    }

    return HitType[key as keyof typeof HitType] as HitType;
  }
}
