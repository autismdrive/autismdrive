import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {MatInput} from '@angular/material/input';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {SearchService} from '../_services/api/search.service';
import {debounce, debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {Subject, timer} from 'rxjs';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent implements OnInit {
  @ViewChild('searchInput', {read: MatInput, static: false}) public searchInput: MatInput;
  words = '';
  queryParams: Params;
  @Input() variant: string;
  searchUpdate = new Subject<String>();

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService
  ) {
    this.route
      .queryParams
      .pipe(debounce(() => timer(1000)))
      .subscribe(qp => this.queryParams = qp);
    this.searchUpdate.pipe(
      debounceTime(400),
      distinctUntilChanged())
      .subscribe(value => {
        console.log(value);
        this.updateSearch(false);
      });
  }

  ngOnInit() {
  }

  isSearchPage(): boolean {
    return (this.router.url.split('/')[1] === 'search');
  }

  showSearch(): void {
    if (this.searchInput) {
      this.searchInput.focus();
    }
  }

  updateSearch(removeWords: boolean): Promise<boolean> {
    if (removeWords) {
      this.words = '';
      this.searchInput.value = this.words;
    }

    const newParams = JSON.parse(JSON.stringify(this.queryParams));
    const words: string = this.searchInput && this.searchInput.value || '';
    newParams.words = removeWords ? undefined : words;
    const hasFilters = Object.keys(newParams).length > 0;

    if (hasFilters) {
      return this.router.navigate(['/search/filter'], {queryParams: newParams});
    } else {
      return this.router.navigateByUrl('/search');
    }
  }

  hasWords(): boolean {
    return this.searchInput && this.searchInput.value && (this.searchInput.value.length > 0);
  }

}
