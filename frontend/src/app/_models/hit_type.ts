export class HitType {

  static LOCATION = new HitType('location', 'Local Services');
  static RESOURCE = new HitType('resource', 'Online Information');
  static EVENT =  new HitType('event', 'Events and Training');
  static STUDY = new HitType('study', 'Research Studies');

  constructor(public name: string, public label: string) {}

  static all(): HitType[] {
    return [this.LOCATION, this.RESOURCE, this.EVENT, this.STUDY];
  }

  static all_resources(): HitType[] {
      return [this.LOCATION, this.RESOURCE, this.EVENT];
  }

}
