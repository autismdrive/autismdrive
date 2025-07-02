/// <reference types="@types/google.analytics" />
import {isPlatformBrowser} from '@angular/common';
import {effect, Inject, Injectable, NgZone, PLATFORM_ID} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {ApiError} from '@app/api-error';
import {Query} from '@app/shared/models/query';
import {Study} from '@app/shared/models/study';
import {AppEnvironmentService} from '@app/shared/services/app-environment/app-environment.service';
import {AuthenticationStateService} from '@app/shared/services/authentication/authentication-state-service';

declare let gtag: Function;

@Injectable({
  providedIn: 'root',
})
export class GoogleAnalyticsService {
  constructor(
    private router: Router,
    private appEnvironmentService: AppEnvironmentService,
    private authenticationStateService: AuthenticationStateService,
    private ngZone: NgZone,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {
    effect(() => {
      if (!this.appEnvironmentService.props() || !isPlatformBrowser(this.platformId)) return;

      this.router.events.subscribe(event => {
        if (event instanceof NavigationEnd) {
          this.ngZone.runOutsideAngular(() => {
            gtag('config', appEnvironmentService.googleAnalyticsTagId, {
              page_path: event.urlAfterRedirects,
            });
          });
        }
      });
    });

    effect(() => {
      const user = this.authenticationStateService.currentUser();
      this.set_user(user || null);
    });
  }

  private event(action: string, category: string, label: string) {
    if (!isPlatformBrowser(this.platformId)) return;
    this.ngZone.runOutsideAngular(() => {
      gtag('event', action, {
        event_category: category,
        event_label: label,
      });
    });
  }

  public errorEvent(error: ApiError) {
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
    if (!isPlatformBrowser(this.platformId)) return;
    this.ngZone.runOutsideAngular(() => {
      gtag('set', {user_id: user_id}); // Set the user ID using signed-in user_id.
    });
  }
}
