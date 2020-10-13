import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-tutorial-video',
  templateUrl: './tutorial-video.component.html',
  styleUrls: ['./tutorial-video.component.scss']
})
export class TutorialVideoComponent implements OnInit {
  @Input() videoSize: string;

  constructor() { }

  ngOnInit() {
  }

  get videoWidth() {
    const baseSize = 560;
    switch (this.videoSize) {
      case 'large':
        return baseSize;
      case 'medium':
        return Math.floor(baseSize * 0.75);
      case 'small':
        return Math.floor(baseSize * 0.5);
    }
  }

  get videoHeight() {
    const baseSize = 315;
    switch (this.videoSize) {
      case 'large':
        return baseSize;
      case 'medium':
        return Math.floor(baseSize * 0.75);
      case 'small':
        return Math.floor(baseSize * 0.5);
    }
  }
}
