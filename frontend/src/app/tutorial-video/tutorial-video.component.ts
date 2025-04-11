/// <reference types="@types/youtube" />
import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {NavItem} from '@models/nav-item';
import {MarkdownModule} from 'ngx-markdown';

@Component({
  standalone: true,
  selector: 'app-tutorial-video',
  templateUrl: './tutorial-video.component.html',
  styleUrls: ['./tutorial-video.component.scss'],
  imports: [MatButtonModule, YouTubePlayerModule, MarkdownModule, DetailsLinkComponent, CommonModule],
})
export class TutorialVideoComponent {
  @Input() videoSize: string;
  @Input() videoId: string;
  @Input() instructions: string;
  @Input() links: NavItem[];
  playerVars: YT.PlayerVars = {
    cc_load_policy: YT.ClosedCaptionsLoadPolicy.ForceOn,
    modestbranding: YT.ModestBranding.Modest,
    rel: YT.RelatedVideos.Hide,
    showinfo: YT.ShowInfo.Hide,
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

  hideVideo() {
    localStorage.setItem('shouldHideTutorialVideo', 'true');
  }
}
