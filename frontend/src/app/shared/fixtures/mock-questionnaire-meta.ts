import {QuestionnaireMeta} from '@models/questionnaire_meta';

export const mockQuestionnaireMeta: QuestionnaireMeta = {
  table: {
    question_type: 'sensitive',
    label: 'Clinical Diagnosis',
  },
  fields: [
    {
      name: 'id',
      key: 'id',
      display_order: 0,
      type: 'string',
    },
  ],
};
