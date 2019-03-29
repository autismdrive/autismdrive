import { Component, OnInit, ViewChild } from '@angular/core';
import { MatInput } from '@angular/material';
import { ActivationEnd, ActivationStart, Router, ActivatedRoute, ActivatedRouteSnapshot } from '@angular/router';
import { User } from './_models/user';
import { AuthenticationService } from './_services/api/authentication-service';
import { SearchService } from './_services/api/search.service';
import { Query } from './_models/query';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'star-drive';
  hideHeader = false;
  currentUser: User;
  searching = false;
  @ViewChild('searchInput', { read: MatInput }) public searchInput: MatInput;

  public constructor(
    private authenticationService: AuthenticationService,
    private router: Router,
    private route: ActivatedRoute,
    private searchService: SearchService
  ) {
    this.router.events.subscribe((e) => {
      if (e instanceof ActivationStart || e instanceof ActivationEnd) {
        if (e.snapshot && e.snapshot.data) {
          const data = e.snapshot.data;
          this.hideHeader = !!data.hideHeader;
        }
      }
    });
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  ngOnInit() {
  }

  goLogout($event: MouseEvent) {
    $event.preventDefault();
    this.authenticationService.logout();
    this.router.navigate(['logout']);
  }

  toggleSearch() {
    this.searching = !this.searching;

    if (this.searching && this.searchInput) {
      this.searchInput.focus();
    }
  }

  updateSearch() {
    const value: string = this.searchInput && this.searchInput.value;

    if (value && (value.length > 0)) {

      // Redirect to search screen if not there yet
      if (this.router.url.split('/')[1] === 'search') {
        const q = this.searchService.currentQueryValue || new Query({});
        q.words = value;
        this.searchService.search(q).subscribe();
      } else {
        this.router.navigateByUrl(`/search/filter?query=${value}`);
      }
    }
  }
}
