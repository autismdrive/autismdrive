// Base class for MultiSelectTreeComponent and FavoriteTopicsDialogComponent
import {Component} from '@angular/core';
import {FieldType, FormlyFieldConfig} from '@ngx-formly/core';
import {NestedTreeControl} from '@angular/cdk/tree';
import {Category} from '@app/_models/category';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {of} from 'rxjs';

@Component({
  selector: 'app-tree',
  template: '',
})
export class TreeComponent extends FieldType<FormlyFieldConfig> {
  dataSource: MatTreeNestedDataSource<Category>;
  treeControl: NestedTreeControl<Category>;

  constructor() {
    super();
    this.treeControl = new NestedTreeControl<Category>(node => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
  }

  findNode(cat_id: number): Category {
    return this.dataSource.data
      .reduce(
        (accumulator: Category[], dataCat: Category) => accumulator.concat(this.treeControl.getDescendants(dataCat)),
        [] as Category[],
      )
      .find(i => i.id === cat_id);
  }
}
