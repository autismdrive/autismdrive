import {CommonModule} from '@angular/common';
import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
import {MatMenuModule} from '@angular/material/menu';
import {MatTooltipModule} from '@angular/material/tooltip';
import {CategoriesById, Category} from '@models/category';
import {ExtendedModule} from '@ngbracket/ngx-layout';
import {CategoriesService} from '@services/categories/categories.service';

@Component({
  standalone: true,
  selector: 'app-search-topics',
  templateUrl: './search-topics.component.html',
  styleUrls: ['./search-topics.component.scss'],
  imports: [
    CommonModule,
    ExtendedModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatMenuModule,
    MatTooltipModule,
  ],
})
export class SearchTopicsComponent {
  @Input() category: Category;
  @Output() categorySelected = new EventEmitter<Category>();
  categoriesById: CategoriesById = {};
  loading = true;

  constructor(
    private categoriesService: CategoriesService,
    private changeDetectorRef: ChangeDetectorRef,
  ) {
    if (this.categoriesService.categoriesById) {
      this.categoriesById = this.categoriesService.categoriesById;
      this.loading = false;
    }

    this.categoriesService.updated.subscribe(() => {
      this.categoriesById = this.categoriesService.categoriesById;
      this.loading = false;
      this.changeDetectorRef.detectChanges();
    });
  }

  get categories() {
    return this.getChildrenWithHits(this.category);
  }

  selectCategory(cat: Category) {
    this.categorySelected.emit(cat);
  }

  parentList(current: Category = this.category, parents: any[] = []): any[] {
    if (current.parent) {
      parents.unshift(current.parent);
      return this.parentList(current.parent, parents);
    } else {
      return parents;
    }
  }

  hasChildren(cat: Category) {
    const category = cat.id === null ? cat : this.categoriesById[cat.id];
    return category && category.children && category.children.length > 0;
  }

  getChildrenWithHits(cat: Category) {
    if (this.hasChildren(cat)) {
      return cat.children.filter(c => c.hit_count > 0);
    } else {
      return [];
    }
  }
}
