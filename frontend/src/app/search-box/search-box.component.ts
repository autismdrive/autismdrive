import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { MatInput } from '@angular/material/input';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { SearchService } from '../_services/api/search.service';
import {debounce, debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {Subject, timer} from 'rxjs';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent implements OnInit {
  @ViewChild('searchInput', { read: MatInput, static: false }) public searchInput: MatInput;
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

  showSearch() {
    if (this.searchInput) {
      this.searchInput.focus();
    }
  }

  updateSearch(removeWords: boolean) {
    if (removeWords) {
      this.words = '';
    }

    console.log('this.searchInput', this.searchInput);


    const newParams = JSON.parse(JSON.stringify(this.queryParams));
    const words: string = this.searchInput && this.searchInput.value || '';
    newParams.words = removeWords ? undefined : words;
    const hasFilters = Object.keys(newParams).length > 0;

    console.log('newParams.words', newParams.words);

    if (hasFilters) {
      this.router.navigate(['/search/filter'], { queryParams: newParams });
    } else {
      this.router.navigateByUrl('/search');
    }
  }

  hasWords(): boolean {
    return this.words && (this.words.length > 0);
  }

}
