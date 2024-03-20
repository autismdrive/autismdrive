import {Component, Input, OnInit} from '@angular/core';
import {NewsItem} from '../_models/news-item';

@Component({
  selector: 'app-news-item',
  templateUrl: './news-item.component.html',
  styleUrls: ['./news-item.component.scss'],
})
export class NewsItemComponent implements OnInit {
  @Input() item: NewsItem;
  @Input() index: number;

  constructor() {}

  ngOnInit() {
    if (!this.item.label) {
      this.item.label = 'Details';
    }
  }

  isEven(i: number) {
    return i % 2 === 0;
  }
}
