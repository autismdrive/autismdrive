/// <reference types="@types/youtube" />
import {Component, Input, OnInit} from '@angular/core';
import {NavItem} from '../_models/nav-item';
import ClosedCaptionsLoadPolicy = YT.ClosedCaptionsLoadPolicy;
import ModestBranding = YT.ModestBranding;
import RelatedVideos = YT.RelatedVideos;
import ShowInfo = YT.ShowInfo;

@Component({
  selector: 'app-tutorial-video',
  templateUrl: './tutorial-video.component.html',
  styleUrls: ['./tutorial-video.component.scss'],
})
export class TutorialVideoComponent implements OnInit {
  @Input() videoSize: string;
  @Input() videoId: string;
  @Input() instructions: string;
  @Input() links: NavItem[];
  playerVars: YT.PlayerVars = {
    cc_load_policy: ClosedCaptionsLoadPolicy.ForceOn,
    modestbranding: ModestBranding.Modest,
    rel: RelatedVideos.Hide,
    showinfo: ShowInfo.Hide,
  };

  constructor() {}

  get windowWidthFactor(): number {
    const windowWidthPx = window.innerWidth;

    if (windowWidthPx < 600) {
      return 0.7;
    } else if (windowWidthPx >= 600 && windowWidthPx < 960) {
      return 0.8;
    } else if (windowWidthPx >= 960 && windowWidthPx < 1280) {
      return 0.9;
    } else if (windowWidthPx >= 1280) {
      return 1.0;
    }
  }

  get videoWidthFactor(): number {
    switch (this.videoSize) {
      case 'large':
        return 1.0;
      case 'medium':
        return 0.75;
      case 'small':
        return 0.5;
    }
  }

  get videoWidth() {
    const baseSize = 560;
    return Math.floor(baseSize * this.videoWidthFactor * this.windowWidthFactor);
  }

  get videoHeight() {
    const baseSize = 315;
    return Math.floor(baseSize * this.videoWidthFactor * this.windowWidthFactor);
  }

  ngOnInit() {}

  hideVideo() {
    localStorage.setItem('shouldHideTutorialVideo', 'true');
  }
}
