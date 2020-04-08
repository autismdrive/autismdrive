export class HitType {

  static labels =
    {
      'location': 'Local Services',
      'resource': 'Online Information',
      'event': 'Events and Training',
      'study': 'Research Studies',
      'all': 'All Results',
      'all_resources': 'All Resources',
    };

  static LOCATION = new HitType('location', HitType.labels.location);
  static RESOURCE = new HitType('resource', HitType.labels.resource);
  static EVENT =  new HitType('event', HitType.labels.event);
  static STUDY = new HitType('study', HitType.labels.study);
  static ALL = new HitType('all', HitType.labels.all);
  static ALL_RESOURCES = new HitType('all_resources', HitType.labels.all_resources);

  constructor(public name: string, public label: string) {}

  static all(): HitType[] {
    return [this.LOCATION, this.RESOURCE, this.EVENT, this.STUDY];
  }

  static all_resources(): HitType[] {
      return [this.ALL_RESOURCES, this.LOCATION, this.RESOURCE, this.EVENT];
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
    };
}

export class Language {
  static labels =
    {
      'english': 'English',
      'spanish': 'Spanish',
      'chinese': 'Chinese',
      'korean': 'Korean',
      'vietnamese': 'Vietnamese',
      'arabic': 'Arabic',
      'tagalog' : 'Tagalog'
    };
}

export class Covid19Categories {
  static labels =
    {
      'COVID-19_for_Autism': 'COVID-19 Information: Information explaining COVID-19 for people with ASD, families and professionals',
      'Health_and_Telehealth': 'Health and Telehealth: Online supports to help support the community\'s mental, behavioral, and ' +
        'physical health',
      'Physical Activity': 'Physical Activity: Resources focused on promoting physical activity and exercise',
      'Visual_Aids': 'Visual Aids: Resources to develop visual schedules, social stories, communication aids explaining COVID-19',
      'Edu-tainment': 'Edu-tainment: Fun educational games, experiences, virtual tours, videos, interactive tools, apps, etc',
      'Supports_with_Living': 'Daily Living Supports: Supports and information related to daily living needs and supporting daily ' +
        'living needs at home (e.g., with family, group care, residential supports)',
      'Free_educational_resources': 'Free Educational Resources: Curriculum based courses, classes, and textbooks; subscriptions'
    };
}
