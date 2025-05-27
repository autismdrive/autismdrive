import {Category} from '@models/category';
import {AgeRange, Language} from '@models/hit_type';
import {Observable} from 'rxjs';

export const getResourceFormFields = (categoryTree: Observable<Category[]> | Category[]) => {
  console.log('getResourceFormFields');
  return [
    {
      key: 'type',
      type: 'select',
      props: {
        label: 'Type',
        options: [
          {value: 'resource', label: 'Online Information'},
          {value: 'location', label: 'Local Services'},
          {value: 'event', label: 'Events and Training'},
        ],
        required: true,
      },
      hideExpression: '!model.createNew',
    },
    {
      key: 'title',
      type: 'input',
      props: {
        label: 'Title',
        placeholder: 'Please enter the title',
        required: true,
      },
      expressionProperties: {
        'props.placeholder': '"Please enter the title of your " + (model.type || "resource")',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'description',
      type: 'textarea',
      props: {
        label: 'Description',
        placeholder: 'Please enter a description',
        description: 'You may use Markdown syntax to insert simple formatting, text links, and images',
        required: true,
      },
      expressionProperties: {
        'props.placeholder': '"Please enter a description of your " + (model.type || "resource")',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'post_event_description',
      type: 'textarea',
      props: {
        label: 'Post-Event Description',
        placeholder: 'Description to display after event has occurred',
        description: 'You may use Markdown syntax to insert simple formatting, text links, and images',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'insurance',
      type: 'textarea',
      props: {
        label: 'Insurance',
        placeholder: 'Please enter the type of insurance if applicable (e.g., private, medicaid, Tricare)',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'includes_registration',
      type: 'radio',
      defaultValue: false,
      props: {
        label: 'Use Autism DRIVE or an external system for registration?',
        description: 'Should users be able to register for this event through Autism DRIVE?',
        options: [
          {value: true, label: 'Autism DRIVE'},
          {value: false, label: 'External system'},
        ],
      },
      expressionProperties: {
        'props.required': 'model.type === "event"',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'registration_url',
      type: 'input',
      props: {
        label: 'Registration Link',
        description: 'If this is left blank, the contact email address will be used for registration.',
        placeholder: 'https://link.to/external/website',
        type: 'url',
      },
      hideExpression: '!(model.type === "event" && !model.includes_registration)',
    },
    {
      key: 'image_url',
      type: 'input',
      props: {
        label: 'Feature Image',
        placeholder: 'https://link.to/external/website/file.jpg',
        type: 'url',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'date',
      type: 'datepicker',
      props: {
        label: 'Event Date',
      },
      expressionProperties: {
        'props.required': 'model.type === "event"',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'time',
      type: 'input',
      props: {
        label: 'Event Time',
        placeholder: 'Please enter the start time or time-frame for your event',
      },
      expressionProperties: {
        'props.required': 'model.type === "event"',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'ticket_cost',
      type: 'input',
      props: {
        label: 'Event Ticket Cost',
        placeholder: 'Please enter the ticket cost for your event',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'webinar_link',
      type: 'input',
      props: {
        label: 'Webinar Link',
        placeholder: 'Please enter the link to attend the webinar',
      },
      hideExpression: 'model.type != "event"',
      validators: {validation: ['url']},
    },
    {
      key: 'post_survey_link',
      type: 'input',
      props: {
        label: 'Survey Link',
        placeholder: 'Please enter the link to the post-event survey',
      },
      hideExpression: 'model.type != "event"',
      validators: {validation: ['url']},
    },
    {
      key: 'max_users',
      type: 'input',
      props: {
        label: 'Maximum attendees',
        placeholder: 'Please enter the maximum number of users allowed to register',
        type: 'number',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'organization_name',
      type: 'input',
      props: {
        label: 'Organization Name',
        placeholder: 'Please enter the name of the organization for your resource',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'primary_contact',
      type: 'input',
      props: {
        label: 'Primary Contact',
        placeholder: 'Please enter the primary contact for your location or event',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'contact_email',
      type: 'input',
      props: {
        label: 'Contact Email',
      },
      validators: {validation: ['email']},
      hideExpression: '!model.type',
      expressionProperties: {
        'props.description': (model, formState, field) => {
          if (model.type === 'event' && !model.includes_registration && !model.registration_link) {
            return 'This contact email will be used for attendees to request information about registering for this event.';
          } else {
            return 'This contact email will not be displayed on the site and is intended for admin use only';
          }
        },
      },
    },
    {
      key: 'location_name',
      type: 'input',
      props: {
        label: 'Location Name',
        placeholder: 'Please enter the name for your event venue',
      },
      hideExpression: 'model.type != "event"',
    },
    {
      key: 'street_address1',
      type: 'input',
      props: {
        label: 'Street Address',
        placeholder: 'Please enter the street address',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'street_address2',
      type: 'input',
      props: {
        label: 'Street Address Details',
        placeholder: 'Please enter any additional details for the street address',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'city',
      type: 'input',
      props: {
        label: 'City',
        placeholder: 'Please enter the city',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'state',
      type: 'input',
      props: {
        label: 'State',
        placeholder: 'Please enter the state',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'zip',
      type: 'input',
      props: {
        label: 'Zip Code',
        placeholder: 'Please enter the zip code',
      },
      hideExpression: '!model.type || model.type == "resource"',
    },
    {
      key: 'phone',
      type: 'input',
      props: {
        label: 'Phone Number',
        placeholder: 'Please enter the phone number',
      },
      hideExpression: '!model.type',
      validators: {validation: ['phone']},
    },
    {
      key: 'phone_extension',
      type: 'input',
      props: {
        label: 'Phone Number Extension',
        placeholder: 'Please enter any extension to the phone number',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'website',
      type: 'input',
      props: {
        label: 'Website',
        placeholder: 'Please enter the website',
      },
      hideExpression: '!model.type',
      validators: {validation: ['url']},
    },
    {
      key: 'video_code',
      type: 'input',
      props: {
        label: 'Video Code',
        placeholder: 'Please enter the YouTube code for a video of this content',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'is_uva_education_content',
      type: 'radio',
      defaultValue: false,
      props: {
        label: 'UVA Education Content',
        description: 'Should this resource be displayed on the UVA Education page?',
        options: [
          {value: true, label: 'Yes'},
          {value: false, label: 'No'},
        ],
      },
      hideExpression: '!model.type',
    },
    {
      key: 'categories',
      type: 'multiselecttree',
      props: {
        label: 'Topics',
        description: 'This field is required',
        options: categoryTree,
        valueProp: 'id',
        labelProp: 'name',
      },
      hideExpression: '!model.type',
    },
    {
      key: 'ages',
      type: 'multicheckbox',
      props: {
        label: 'Age Ranges',
        type: 'array',
        options: AgeRange.options,
      },
      hideExpression: '!model.type',
    },
    {
      key: 'languages',
      type: 'multicheckbox',
      props: {
        label: 'Languages',
        type: 'array',
        options: Language.options,
      },
      hideExpression: '!model.type',
    },
    {
      key: 'should_hide_related_resources',
      type: 'radio',
      defaultValue: false,
      props: {
        label: 'Hide Related Resources',
        description: 'Should related resources be displayed alongside this resource on the details page?',
        options: [
          {value: true, label: 'Yes'},
          {value: false, label: 'No'},
        ],
      },
      hideExpression: '!model.type',
    },
  ];
};
