/// <reference types="@types/youtube" />
import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {YouTubePlayerModule} from '@angular/youtube-player';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {NavItem} from '@models/nav-item';
import {StorageService} from '@services/storage/storage.service';
import {WindowService} from '@services/window/window.service';
import {MarkdownModule} from 'ngx-markdown';

@Component({
  standalone: true,
  selector: 'app-tutorial-video',
  templateUrl: './tutorial-video.component.html',
  styleUrls: ['./tutorial-video.component.scss'],
  imports: [MatButtonModule, MatIconModule, MarkdownModule, DetailsLinkComponent, CommonModule, YouTubePlayerModule],
})
export class TutorialVideoComponent {
  @Input() videoSize: string;
  @Input() videoId: string;
  @Input() instructions: string;
  @Input() links: NavItem[];
  playerVars: YT.PlayerVars = {
    cc_load_policy: 1, // YT.ClosedCaptionsLoadPolicy.ForceOn
    modestbranding: 1, // YT.ModestBranding.Modest
    rel: 0, // YT.RelatedVideos.Hide
    showinfo: 0, // YT.ShowInfo.Hide
  };

  constructor(
    private storageService: StorageService,
    private windowService: WindowService,
  ) {}

  get windowWidthFactor(): number {
    const windowWidthPx = this.windowService.window.innerWidth;

    if (windowWidthPx < 600) {
      return 0.7;
    } else if (windowWidthPx >= 600 && windowWidthPx < 960) {
      return 0.8;
    } else if (windowWidthPx >= 960 && windowWidthPx < 1280) {
      return 0.9;
    } else if (windowWidthPx >= 1280) {
      return 1.0;
    } else {
      return 1.0;
    }
  }

  get videoWidthFactor(): number {
    switch (this.videoSize) {
      case 'large':
        return 1.0;
      case 'medium':
      default:
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
    this.storageService.set('shouldHideTutorialVideo', 'true');
  }
}
