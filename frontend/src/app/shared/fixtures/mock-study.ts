import {faker} from '@faker-js/faker';
import {Study, StudyProps, StudyStatus} from '@models/study';

export const makeMockStudy = (overrideProps?: Partial<StudyProps>): Study => {
  const defaultProps: StudyProps = {
    id: faker.number.int(),
    title: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    short_title: faker.commerce.productAdjective(),
    short_description: faker.commerce.productMaterial(),
    participant_description: faker.person.jobTitle(),
    benefit_description: faker.company.buzzPhrase(),
    investigators: [],
    organization_name: faker.company.name(),
    location: faker.airline.airport().name,
    categories: [],
    status: StudyStatus.currently_enrolling,
    num_visits: faker.number.int(),
    coordinator_email: faker.internet.email(),
    study_categories: [],
    study_investigators: [],
    image_url: faker.internet.url(),
    eligibility_url: faker.internet.url(),
    survey_url: faker.internet.url(),
    results_url: faker.internet.url(),
    ages: [],
    languages: [],
    last_updated: faker.date.past(),
  };

  return new Study({...defaultProps, ...overrideProps});
};

export const mockStudy: Study = makeMockStudy();
