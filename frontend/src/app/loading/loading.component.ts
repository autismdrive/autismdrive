import {CommonModule} from '@angular/common';
import {Component, Input, OnInit} from '@angular/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSelectModule} from '@angular/material/select';
import {FlexModule} from '@ngbracket/ngx-layout';

@Component({
  standalone: true,
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.scss'],
  imports: [CommonModule, MatProgressSpinnerModule, FlexModule, MatFormFieldModule, MatSelectModule],
})
export class LoadingComponent implements OnInit {
  @Input() showSpinner = true;
  @Input() message: string;
  @Input() size = 'lg';
  @Input() baseSize = 24;
  @Input() isField = false;

  get diameter(): number {
    switch (this.size) {
      case 'xl':
        return this.baseSize * 4;
      case 'lg':
        return this.baseSize * 3;
      case 'med':
        return this.baseSize * 2;
      case 'sm':
        return this.baseSize;
      default:
        return this.baseSize * 3;
    }
  }

  constructor() {}

  ngOnInit(): void {}
}
