import {faker} from '@faker-js/faker';
import {TableInfo} from '@models/table_info';

export const mockQuestionnaireInfoList: TableInfo[] = [
  new TableInfo({
    display_name: 'some_display_name',
    table_name: 'some_table_name',
    class_name: 'some_class_name',
    size: faker.number.int(),
    url: faker.internet.url(),
    question_type: 'some_question_type',
    exportable: true,
    sub_tables: [],
  }),
];
