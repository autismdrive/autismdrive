import { Resource } from '../../resource';
import { Institution } from '../../institution';

const institution: Institution = { id: 777, name: 'The Old Republic' };

export function getDummyResource(): Resource {
  return {
    id: 999,
    name: 'R2-D2',
    description: 'Has seen things you people wouldn\'t believe: Attack ships on fire off the shoulder of Orion...',
    owner: 'queen-amidala@naboo.gov, obi.wan@jedi-temple.net, capt.antilles@mil.alderaan.gov',
    owners: ['queen-amidala@naboo.gov', 'obi.wan@jedi-temple.net', 'capt.antilles@mil.alderaan.gov'],
    contact_email: 'r2d2@rebels.org',
    contact_notes: 'Ask about the Clone Wars.',
    contact_phone: '975-310-8642',
    cost: 'More than you can afford',
    favorite_count: 888,
    institution_id: 777,
    type_id: 666,
    website: 'https://www.rebels.org/r2d2',
    approved: 'Unapproved',
    user_may_view: false,
    user_may_edit: false,
    last_updated: '1977-05-25T00:00:000Z',
    favorites: [],
    availabilities: [{
      institution_id: 0,
      resource_id: 999,
      available: true,
      institution: institution
    }],
    institution: institution
  };
}
