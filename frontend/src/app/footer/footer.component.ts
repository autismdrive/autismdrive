import {BreakpointObserver} from '@angular/cdk/layout';
import {NgIf, NgOptimizedImage} from '@angular/common';
import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {ImageDimensions} from '@models/image-dimensions';
import {ConfigService} from '@services/config/config.service';

@Component({
  standalone: true,
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
  imports: [NgIf, NgOptimizedImage],
})
export class FooterComponent {
  logoURL = '/assets/logo/UVA_STAR-logo.svg';
  logoDimensions: ImageDimensions;

  constructor(
    public config: ConfigService,
    public router: Router,
    private breakpointObserver: BreakpointObserver,
  ) {
    this.breakpointObserver.observe('(max-width: 959px)').subscribe(result => {
      const ratio = result ? 0.51 : 0.72;
      this.logoDimensions = {width: ratio * 300, height: ratio * 74};
    });
  }
}
