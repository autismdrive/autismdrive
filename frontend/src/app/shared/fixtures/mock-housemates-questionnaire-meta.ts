export const mockHousematesQuestionnaireMeta = {
  type: 'repeat',
  display_order: 3,
  wrappers: ['card'],
  props: {
    label: 'Who else lives with you?',
    description: 'Add a housemate',
  },
  expression_properties: {},
  name: 'housemates',
  key: 'housemates',
  fieldArray: {
    fieldGroup: [
      {
        display_order: 3.1,
        type: 'input',
        props: {
          label: 'Name',
          required: true,
        },
        name: 'name',
        key: 'name',
      },
      {
        display_order: 3.2,
        type: 'select',
        props: {
          required: false,
          label: 'Relationship',
          placeholder: 'Please select',
          options: [
            {
              value: 'bioParent',
              label: 'Biological Parent',
            },
            {
              value: 'bioSibling',
              label: 'Biological Sibling',
            },
            {
              value: 'stepParent',
              label: 'Step Parent',
            },
            {
              value: 'stepSibling',
              label: 'Step Sibling',
            },
            {
              value: 'adoptParent',
              label: 'Adoptive Parent',
            },
            {
              value: 'adoptSibling',
              label: 'Adoptive Sibling',
            },
            {
              value: 'spouse',
              label: 'Spouse',
            },
            {
              value: 'significantOther',
              label: 'Significant Other',
            },
            {
              value: 'child',
              label: 'Child',
            },
            {
              value: 'roommate',
              label: 'Roommate',
            },
            {
              value: 'paidCaregiver',
              label: 'Paid Caregiver',
            },
            {
              value: 'relationOther',
              label: 'Other',
            },
          ],
        },
        expression_properties: {
          'props.label': '"Relationship to you"',
        },
        name: 'relationship',
        key: 'relationship',
      },
      {
        display_order: 3.3,
        type: 'input',
        props: {
          label: 'Please enter their relationship',
          required: true,
        },
        hide_expression: '!(model.relationship && (model.relationship === "relationOther"))',
        expression_properties: {
          'props.required': '!!(model.relationship && (model.relationship === "relationOther"))',
        },
        name: 'relationship_other',
        key: 'relationship_other',
      },
      {
        display_order: 3.4,
        type: 'input',
        props: {
          label: 'Age',
          type: 'number',
          max: 130,
          required: true,
        },
        validation: {
          messages: {
            max: 'Please enter age in years',
          },
        },
        name: 'age',
        key: 'age',
      },
      {
        display_order: 3.5,
        type: 'radio',
        props: {
          label: 'Does this relation have autism?',
          required: false,
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
        name: 'has_autism',
        key: 'has_autism',
      },
    ],
  },
};
