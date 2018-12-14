import { Category } from '../../category';
import { Icon } from '../../icon';

const icon: Icon = {
  id: 0,
  name: 'robot',
  url: 'https://bleep.blorp.galaxy.com/icons/robot'
};

const grandParent: Category = {
  id: 0,
  parent_id: null,
  level: 0,
  name: 'Individuals',
  brief_description: 'That which exists as a distinct entity',
  description: `
> This above all: to thine own self be true,
> And it must follow, as the night the day,
> Thou canst not then be false to any man.
> Farewell, my blessing season this in thee!
–William Shakespeare, *Hamlet*`,
  color: '#123456',
  children: [],
  icon_id: 'robot',
  image: '',
  resource_count: 1,
  display_order: 0,
  icon: icon
};

const parent: Category = {
  id: 12,
  parent_id: 0,
  level: 1,
  name: 'Technology',
  brief_description: 'Any sufficiently advanced technology is indistinguishable from magic.',
  description: `
> Sometimes a thousand twangling instruments
> Will hum about mine ears; and sometime voices
> That if I then had waked after long sleep
> Will make me sleep again; and then, in dreaming
> The clouds methought would open and show riches
> Ready to drop upon me, that, when I waked,
> I cried to dream again.
–William Shakespeare, *The Tempest*`,
  color: '#123456',
  children: [],
  icon_id: '',
  image: '',
  resource_count: 1,
  display_order: 0,
  parent: grandParent,
  icon: icon
};

export function getDummyCategory(): Category {
  return {
    id: 123,
    parent_id: 12,
    level: 2,
    name: 'Droids',
    brief_description: 'Human-cyborg relations',
    description: `
> Around both humans and droids I must
> Be seen to make such errant beeps and squeaks
> That they shall think me simple. Truly, though,
> Although with sounds obilque I speak to them,
> I clearly see how I shall play my part,
> And how a vast rebellion shall succeed
> by wit and wisdom of a simple droid.
–Ian Doescher, *William Shakespeare's Star Wars: Verily, A New Hope*`,
    color: '#123456',
    children: [],
    icon_id: '',
    image: '',
    resource_count: 1,
    display_order: 0,
    parent: parent
  };
}
