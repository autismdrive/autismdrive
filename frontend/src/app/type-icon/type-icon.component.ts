import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-type-icon',
  templateUrl: './type-icon.component.html',
  styleUrls: ['./type-icon.component.scss']
})
export class TypeIconComponent implements OnInit {
  @Input() iconType: string;
  @Input() size: number;

  constructor() { }

  ngOnInit() {
  }

}
