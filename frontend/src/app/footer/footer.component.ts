import {Component} from '@angular/core';
import {ConfigService} from '../_services/config/config.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  constructor(
    public config: ConfigService,
    public router: Router,
  ) {}

}
