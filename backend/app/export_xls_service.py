# Thanks to https://gist.github.com/piersstorey/b32583f0cc5cba0a38a11c2b123af687
import os
import io
import re

import xlsxwriter
from flask import Response
from datetime import datetime
from werkzeug.datastructures import Headers
from app.export_service import ExportService


class ExportXlsService:

    @staticmethod
    def get_questionnaire_names(app):
        all_file_names = os.listdir(os.path.dirname(app.instance_path) + '/app/model/questionnaires')
        non_questionnaires = ['mixin', '__']
        questionnaire_file_names = []
        for index, file_name in enumerate(all_file_names):
            if any(string in file_name for string in non_questionnaires):
                pass
            else:
                f = file_name.replace(".py", "")
                questionnaire_file_names.append(ExportService.camel_case_it(f))
        return sorted(questionnaire_file_names)

    @staticmethod
    def pretty_title_from_snakecase(title):
        # Capitalizes, removes '_', drops 'Questionnaire' and limits to 30 chars.
        title = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', title)
        title = re.sub('([a-z0-9])([A-Z])', r'\1 \2', title)
        return title.replace("Questionnaire", "").strip()[:30]

    @staticmethod
    def export_xls(name, app, user_id=None):
        # Flask response
        response = Response()
        response.status_code = 200

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        if name.lower() == 'all':
            # Get Questionnaire Names
            questionnaire_names = ExportXlsService.get_questionnaire_names(app)
        else:
            cl = ExportService.get_class(name)
            info = ExportService.get_single_table_info(cl, None)
            questionnaire_names = [name]
            for sub_table in info.sub_tables:
                questionnaire_names.append(sub_table.class_name)

        # Create workbook
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        for qname in questionnaire_names:
            worksheet = workbook.add_worksheet(ExportXlsService.pretty_title_from_snakecase(qname))
            # Some data we want to write to the worksheet.
            # Get header fields from the schema in case the first record is missing fields
            schema = ExportService.get_schema(qname, many=True)
            header_fields = schema.fields
            if user_id:
                questionnaires = schema.dump(ExportService().get_data(name=qname, user_id=user_id))
            else:
                questionnaires = schema.dump(ExportService().get_data(name=qname))

            # Start from the first cell. Rows and columns are zero indexed.
            row = 0
            col = 0

            # Write the column headers.
            for key in header_fields:
                worksheet.write(row, col, key, bold)
                col += 1
            row += 1

            # Iterate over the data and write it out row by row.
            for item in questionnaires[0]:
                col = -1
                for key in item:
                    if key == "_links":
                        continue
                    if isinstance(item[key], dict):
                        continue
                    if isinstance(item[key], list) and len(item[key]) > 0 and isinstance(item[key][0], dict):
                        continue # Don't try to represent sub-table data.
                    if isinstance(item[key], list):
                        list_string = ''
                        for value in item[key]:
                            list_string = list_string + str(value) + ', '
                        col += 1
                        worksheet.write(row, col, list_string)
                    else:
                        col += 1
                        worksheet.write(row, col, item[key])
                row += 1

        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Add output to response
        response.data = output.read()

        # Set filname
        file_name = 'export_{}_{}.xlsx'.format(name, datetime.now())

        # HTTP headers for forcing file download
        response_headers = Headers({
            'Pragma': "public",  # required,
            'Expires': '0',
            'Cache-Control': 'must-revalidate, private',  # required for certain browsers
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
            'Content-Transfer-Encoding': 'binary',
            'Access-Control-Expose-Headers': 'x-filename',
            'x-filename': file_name,
            'Content-Length': len(response.data)
        })

        # Add headers
        response.headers = response_headers

        # jquery.fileDownload.js requirements
        response.set_cookie('fileDownload', 'true', path='/')

        # Return the response
        return response


