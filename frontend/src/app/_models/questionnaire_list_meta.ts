export interface QuestionnaireListMeta {
  table: {
    question_type: string;
    label: string;
  };
  fields: Array<{
    name: string;
    key: string;
    display_order: number;
  }>;
}
