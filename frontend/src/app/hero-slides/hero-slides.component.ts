import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatTooltipModule} from '@angular/material/tooltip';
import {RouterModule} from '@angular/router';
import {NewsItem} from '@models/news-item';
import {IntervalService} from '@services/interval/interval.service';

@Component({
  standalone: true,
  selector: 'app-hero-slides',
  templateUrl: './hero-slides.component.html',
  styleUrls: ['./hero-slides.component.scss'],
  imports: [CommonModule, MatTooltipModule, RouterModule],
})
export class HeroSlidesComponent {
  @Input() slides: NewsItem[];
  activeIndex = 0;
  delayMs = 5000;

  constructor(private intervalService: IntervalService) {
    intervalService.setInterval(() => {
      this._incrementActiveIndex();
    }, this.delayMs);
  }

  _incrementActiveIndex() {
    if (this.activeIndex < this.slides.length - 1) {
      this.activeIndex++;
    } else {
      this.activeIndex = 0;
    }
  }

  setActiveSlide(slideIndex: number) {
    this.activeIndex = slideIndex;

    // Reset the timer
    this.intervalService.clearInterval();
    this.intervalService.setInterval(() => {
      this._incrementActiveIndex();
    }, this.delayMs);
  }

  activeClass(slideIndex: number): string {
    if (slideIndex === this.activeIndex) {
      return 'active';
    } else {
      if (this.activeIndex === this.slides.length - 1) {
        // Last slide
        // On last slide, first slide is next
        return slideIndex === 0 ? 'next' : 'prev';
      } else if (this.activeIndex === 0) {
        // First slide
        // On first slide, last slide is prev
        return slideIndex === this.slides.length - 1 ? 'prev' : 'next';
      } else {
        // Middle slide
        return slideIndex < this.activeIndex ? 'prev' : 'next';
      }
    }
  }
}
