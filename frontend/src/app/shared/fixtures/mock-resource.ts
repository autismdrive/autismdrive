import {Resource, ResourceProps, ResourceType} from '@models/resource';
import {faker} from '@faker-js/faker';

export const makeMockResource = (overrideProps?: Partial<ResourceProps>): Resource => {
  const defaultProps: ResourceProps = {
    type: ResourceType.RESOURCE,
    title: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    post_event_description: faker.company.buzzPhrase(),
    insurance: faker.company.buzzNoun(),
    date: faker.date.soon().toISOString(),
    time: faker.date.soon().toTimeString(),
    ticket_cost: faker.commerce.price(),
    organization_name: faker.company.name(),
    primary_contact: faker.person.fullName(),
    location_name: faker.company.buzzNoun(),
    street_address1: faker.location.streetAddress(),
    street_address2: '',
    city: faker.location.city(),
    state: faker.location.state(),
    zip: faker.location.zipCode(),
    phone: faker.phone.number(),
    phone_extension: faker.number.int().toString(),
    website: faker.internet.url(),
    contact_email: faker.internet.email(),
    video_code: '',
    is_uva_education_content: true,
    is_draft: false,
    last_updated: faker.date.past().toISOString(),
    status: '',
    resource_categories: [],
    categories: [],
    ages: [],
    languages: [],
    covid19_categories: [],
    includes_registration: true,
    webinar_link: faker.internet.url(),
    post_survey_link: faker.internet.url(),
    max_users: faker.number.int({min: 10, max: 1000}),
    image_url: faker.internet.url(),
    registration_url: faker.internet.url(),
    should_hide_related_resources: false,
  };

  return new Resource({...defaultProps, ...overrideProps});
};

export const mockResource: Resource = makeMockResource();
