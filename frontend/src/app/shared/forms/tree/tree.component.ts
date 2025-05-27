/**
 * Base class for MultiSelectTreeComponent and FavoriteTopicsDialogComponent
 */
import {AfterContentChecked, ChangeDetectionStrategy, Component} from '@angular/core';
import {MatNestedTreeNode, MatTreeModule, MatTreeNestedDataSource} from '@angular/material/tree';
import {Category, CatTreeNode, CatTreeNodeList} from '@app/shared/models/category';
import {FormlyFieldConfig} from '@ngx-formly/core';
import {FieldType} from '@ngx-formly/material';
import {lastValueFrom, Observable, of} from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-tree',
  template: '',
  imports: [MatTreeModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TreeComponent extends FieldType<FormlyFieldConfig> implements AfterContentChecked {
  dataSource: MatTreeNestedDataSource<Category>;
  treeControl: MatNestedTreeNode<Category>;
  catMap: Map<number, CatTreeNode> = new Map();

  constructor() {
    console.log('TreeComponent > constructor');
    super();
    this.treeControl = new MatNestedTreeNode<Category>((node: Category) => of(node.children));
    this.dataSource = new MatTreeNestedDataSource();
  }

  ngAfterContentChecked() {
    this.getDescendants(this.treeControl).then(descendants => {
      descendants.forEach(d => this.catMap.set(d.data.id, d));
    });
  }

  /** Returns a flattened array of all descendant nodes for the given node. */
  async getDescendants(node: CatTreeNode) {
    const _collectDescendants = async (_node: CatTreeNode, _accumulator: CatTreeNode[]) => {
      _accumulator.push(_node);
      const _obs: CatTreeNodeList = _node.getChildren();
      const catTreeNodes: CatTreeNode[] = _obs instanceof Observable ? await lastValueFrom(_obs) : _obs;

      for (const c of catTreeNodes) {
        await _collectDescendants(c, _accumulator);
      }

      return _accumulator;
    };

    return _collectDescendants(node, []);
  }

  /** Returns the Category from the tree that matches the given Category ID. */
  findNode(catId: number): CatTreeNode {
    return this.catMap.get(catId);
  }

  childrenAccessor = (dataNode: Category) => dataNode.children ?? [];

  hasNestedChild = (_: number, node: Category) => node?.children?.length > 0;
}
