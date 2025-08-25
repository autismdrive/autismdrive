import {faker} from '@faker-js/faker';
import {EmailLog} from '@models/email_log';

export const makeMockEmailLog = (overrides?: Partial<EmailLog>): EmailLog => {
  return {
    id: faker.number.int(),
    user_id: faker.number.int(),
    type: faker.helpers.arrayElement(['reset_email', 'study_inquiry_email', 'confirm_email']),
    tracking_code: faker.helpers.fromRegExp(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{2}/),
    viewed: false,
    date_viewed: faker.date.recent().toISOString(),
    ...overrides,
  };
};

export const mockEmailLog: EmailLog = makeMockEmailLog();
