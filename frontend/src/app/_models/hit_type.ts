export class HitType {

  static labels =
    {
      'location': 'Local Services',
      'resource': 'Online Information',
      'event': 'Events and Training',
      'study': 'Research Studies'
    };

  static LOCATION = new HitType('location', HitType.labels.location);
  static RESOURCE = new HitType('resource', HitType.labels.resource);
  static EVENT =  new HitType('event', HitType.labels.event);
  static STUDY = new HitType('study', HitType.labels.study);

  constructor(public name: string, public label: string) {}

  static all(): HitType[] {
    return [this.LOCATION, this.RESOURCE, this.EVENT, this.STUDY];
  }

  static all_resources(): HitType[] {
      return [this.LOCATION, this.RESOURCE, this.EVENT];
  }
}

export class AgeRange {
  static labels =
    {
      'pre-k': 'Pre-K (0 - 5 years)',
      'school': 'School Age (6 - 13 years)',
      'transition': 'Transition Age (14 - 22 years)',
      'adult': 'Adulthood (23 - 64)',
      'aging': 'Aging (65+)'
    }
}