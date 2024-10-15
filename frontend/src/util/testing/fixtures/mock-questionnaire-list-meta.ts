import {QuestionnaireListMeta} from '@models/questionnaire_list_meta';

export const mockQuestionnaireListMeta: QuestionnaireListMeta = {
  table: {
    question_type: 'sensitive',
    label: 'Clinical Diagnosis',
  },
  fields: [
    {
      name: 'id',
      key: 'id',
      display_order: 0,
    },
  ],
};
