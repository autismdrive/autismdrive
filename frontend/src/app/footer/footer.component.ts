import {CommonModule, NgOptimizedImage} from '@angular/common';
import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {ImageDimensions} from '@models/image-dimensions';
import {AppEnvironmentService} from '@services/app-environment/app-environment.service';

@Component({
  standalone: true,
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
  imports: [CommonModule, NgOptimizedImage],
})
export class FooterComponent {
  logoURL = '/public/logo/UVA_STAR-logo.svg';
  logoDimensions: ImageDimensions;

  constructor(
    public config: AppEnvironmentService,
    public router: Router,
  ) {}
}
