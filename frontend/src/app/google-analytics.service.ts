import {Injectable} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {ConfigService} from './_services/config.service.ts/config';

declare var gtag: Function;

@Injectable({
  providedIn: 'root'
})
export class GoogleAnalyticsService {

  constructor(private router: Router, private configService: ConfigService) {
  }

  public event(eventName: string, params: {}) {
    gtag('event', eventName, params);
  }

  public set_user(user_id) {
    gtag('set', {'user_id': user_id}); // Set the user ID using signed-in user_id.
  }

  public init() {
    this.listenForRouteChanges();

    try {
      const analysticsKey = this.configService.googleAnalyticsKey;

      const script1 = document.createElement('script');
      script1.async = true;
      script1.src = 'https://www.googletagmanager.com/gtag/js?id=' + analysticsKey;
      document.head.appendChild(script1);

      const script2 = document.createElement('script');
      script2.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '` + analysticsKey + `', {'send_page_view': false});
      `;
      document.head.appendChild(script2);
    } catch (ex) {
      console.error('Error appending google analytics');
      console.error(ex);
    }
  }

  private listenForRouteChanges() {
    const analyticsKey = this.configService.googleAnalyticsKey;
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        gtag('config', analyticsKey, {
          'page_path': event.urlAfterRedirects,
        });
      }
    });
  }
}
