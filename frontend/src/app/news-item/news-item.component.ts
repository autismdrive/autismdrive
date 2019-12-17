import { Component, OnInit, Input } from '@angular/core';
import { NewsItem } from '../_models/news-item';

@Component({
  selector: 'app-news-item',
  templateUrl: './news-item.component.html',
  styleUrls: ['./news-item.component.scss']
})
export class NewsItemComponent implements OnInit {
  @Input() item: NewsItem;
  @Input() index: number;

  constructor() { }

  ngOnInit() {
  }

  isEven(i: number) {
    return i % 2 === 0;
  }

  itemLabel() {
    if (this.item.url.substr(-6,6) == '+video') {
      return "Watch this video"
    } else {
      return "Details"
    }
  }
}
