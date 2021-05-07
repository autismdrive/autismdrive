export class UserMeta {
  user_id?: number;
  self_has_guardian: boolean;
  self_own_guardian: boolean;
  guardian_legal: boolean;
  guardian_not_legal: boolean;
  professional: boolean;
  interested:  boolean;

  constructor(private _props) {
    for (const propName in this._props) {
      if (this._props.hasOwnProperty(propName)) {
        this[propName] = this._props[propName];
      }
    }
  }
  getMetaData(): string {
    if (this.self_own_guardian) {
      return 'self_own_guardian';
    } else if (this.guardian_legal) {
      return 'guardian_legal';
    } else if (this.professional) {
      return 'professional';
    } else if (this.guardian_not_legal) {
      return 'guardian_not_legal';
    } else if (this.self_has_guardian) {
      return 'self_has_guardian';
    } else if (this.interested) {
      return 'interested';
    } else { return 'no_meta_data'; }
  }

}
