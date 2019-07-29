export class TableInfo {
  display_name: string;
  table_name: string;
  class_name: string;
  size: number;
  url: string;
  question_type: string;
  exportable: boolean;
  sub_tables: TableInfo[];

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }

  getIcon(): string {
    switch (this.question_type) {
      case 'sensitive': {
        return 'vpn_key';
      }
      case 'identifying': {
        return 'fingerprint';
      }
      case 'unrestricted': {
        return 'remove';
      }
      default: {
        return 'remove';
      }
    }
  }

}
