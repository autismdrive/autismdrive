import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {ConfigService} from '../_services/config/config.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
  constructor(
    public config: ConfigService,
    public router: Router,
  ) {}
}
