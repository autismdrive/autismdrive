export const mockIdentificationQuestionnaireMeta = [
  {
    fields: [],
    display_order: 1,
    wrappers: ['help'],
    props: {
      description: 'Please answer the following questions about yourself (* indicates required response):',
    },
    name: 'intro',
  },
  {
    display_order: 2,
    type: 'input',
    props: {
      label: 'First name',
      required: true,
    },
    name: 'first_name',
    key: 'first_name',
  },
  {
    display_order: 3,
    type: 'input',
    props: {
      label: 'Middle name',
    },
    hide_expression: 'model.no_middle_name',
    expression_properties: {
      'props.required': '!model.no_middle_name',
    },
    name: 'middle_name',
    key: 'middle_name',
  },
  {
    display_order: 3.5,
    type: 'checkbox',
    default_value: false,
    props: {
      label: 'If NO Middle Name click here',
      required: false,
    },
    name: 'no_middle_name',
    key: 'no_middle_name',
  },
  {
    display_order: 4,
    type: 'input',
    props: {
      label: 'Last name',
      required: true,
    },
    name: 'last_name',
    key: 'last_name',
  },
  {
    display_order: 5,
    type: 'radio',
    props: {
      required: false,
      label: 'Is this your preferred name?',
      options: [
        {
          value: true,
          label: 'Yes',
        },
        {
          value: false,
          label: 'No',
        },
      ],
    },
    name: 'is_first_name_preferred',
    key: 'is_first_name_preferred',
  },
  {
    display_order: 6,
    type: 'input',
    props: {
      label: 'Nickname',
      required: false,
    },
    hide_expression: 'model.is_first_name_preferred',
    name: 'nickname',
    key: 'nickname',
  },
  {
    display_order: 7,
    type: 'datepicker',
    props: {
      required: true,
      label: 'Your date of birth',
    },
    name: 'birthdate',
    key: 'birthdate',
  },
  {
    display_order: 8,
    type: 'input',
    props: {
      required: true,
      label: 'Your city/municipality of birth',
    },
    name: 'birth_city',
    key: 'birth_city',
  },
  {
    display_order: 9,
    type: 'input',
    props: {
      required: true,
      label: 'Your state of birth',
    },
    name: 'birth_state',
    key: 'birth_state',
  },
  {
    display_order: 10,
    type: 'radio',
    props: {
      required: false,
      label: 'Is your primary language English?',
      options: [
        {
          value: true,
          label: 'Yes',
        },
        {
          value: false,
          label: 'No',
        },
      ],
    },
    name: 'is_english_primary',
    key: 'is_english_primary',
  },
];
