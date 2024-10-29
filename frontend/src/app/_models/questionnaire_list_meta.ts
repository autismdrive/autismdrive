export interface QuestionnaireListMeta {
  table: {
    question_type: string;
    label: string;
  };
  fields: {
    name: string;
    key: string;
    display_order: number;
  }[];
}
