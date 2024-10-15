import {Injectable} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {StarError} from '@app/star-error';
import {Query} from '@models/query';
import {Study} from '@models/study';
import {ConfigService} from '@services/config/config.service';

declare var gtag: Function;

@Injectable({
  providedIn: 'root',
})
export class GoogleAnalyticsService {
  constructor(
    private router: Router,
    private configService: ConfigService,
  ) {}

  private event(action: string, category: string, label: string) {
    gtag('event', action, {
      event_category: category,
      event_label: label,
    });
  }

  public errorEvent(error: StarError) {
    this.event(error.code, 'error_messages', error.message);
  }

  public accountEvent(eventName: string) {
    this.event(eventName, 'account', '');
  }

  public searchEvent(query: Query) {
    if (query.words) {
      this.event(query.words, 'search', '');
    }
    for (const age of query.ages) {
      this.event(age.toString(), 'search_filter', '');
    }
    if (query.category) {
      this.event(query.category.name, 'search_filter', 'search_topic');
    }
    if (query.types.length === 1) {
      this.event(query.types[0].toString(), 'search_filter', '');
    }
    this.event(query.sort.field, 'search_sort', '');

    this.event(query.start.toString(), 'search_start', '');
  }

  public searchInteractionEvent(eventName: string) {
    this.event(eventName, 'search_interaction', '');
  }

  public mapEvent(windowId: string) {
    this.event(windowId, 'map_interaction', 'map_pin_click');
  }

  public mapResourceEvent(resourceId: string) {
    this.event(resourceId, 'map_interaction', 'map_pin_resource_click');
  }

  public studyInquiryEvent(study: Study) {
    this.event(study.id.toString(), 'study_inquiry', study.title);
  }

  public studySurveyEvent(study: Study) {
    this.event(study.id.toString(), 'study_survey', study.title);
  }

  public flowStartEvent(flowName: string) {
    this.event(flowName, 'flow_started', '');
  }

  public flowCompleteEvent(flowName: string) {
    this.event(flowName, 'flow_completed', '');
  }

  public stepCompleteEvent(stepName: string) {
    this.event(stepName, 'step_completed', '');
  }

  public relatedContentEvent(eventName: string, parentComponent: string) {
    this.event(eventName, 'related_content', parentComponent);
  }

  public set_user(user_id) {
    gtag('set', {user_id: user_id}); // Set the user ID using signed-in user_id.
  }

  public init() {
    this.listenForRouteChanges();

    try {
      const apiKey = this.configService.googleAnalyticsKey;

      const script1 = document.createElement('script');
      script1.async = true;
      script1.src = 'https://www.googletagmanager.com/gtag/js?id=' + apiKey;
      document.head.appendChild(script1);

      const script2 = document.createElement('script');
      script2.innerHTML =
        `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '` +
        apiKey +
        `', {'send_page_view': false});
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
          page_path: event.urlAfterRedirects,
        });
      }
    });
  }
}
