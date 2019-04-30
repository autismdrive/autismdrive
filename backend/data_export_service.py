# Thanks to https://gist.github.com/piersstorey/b32583f0cc5cba0a38a11c2b123af687
import os
import io
import xlsxwriter
from flask import Response
from datetime import datetime
from werkzeug.datastructures import Headers
from app import db
from app.question_service import QuestionService


def get_questionnaire_data(name):
    class_ref = QuestionService.get_class(name)
    schema = QuestionService.get_schema(name, many=True)
    q = db.session.query(class_ref).all()
    return schema.dump(q)


def get_questionnaire_fields(name):
    return QuestionService.get_schema(name).fields


def get_questionnaire_names():
    all_file_names = os.listdir('./app/model/questionnaires')
    non_questionnaires = ['mixin', '__']
    questionnaire_file_names = []
    for index, file_name in enumerate(all_file_names):
        if any(string in file_name for string in non_questionnaires):
            pass
        else:
            f = file_name.replace(".py", "")
            questionnaire_file_names.append(f)
    return sorted(questionnaire_file_names)


class DataExport:
    def export(name):
        # Flask response
        response = Response()
        response.status_code = 200

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        if name == 'all':
            # Get Questionnaire Names
            questionnaire_names = get_questionnaire_names()
        else:
            questionnaire_names = [name]

        # Create workbook
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        for qname in questionnaire_names:
            worksheet = workbook.add_worksheet(qname[:30])

            # Some data we want to write to the worksheet.
            # Get header fields from the schema in case the first record is missing fields
            header_fields = get_questionnaire_fields(name=qname)
            questionnaires = get_questionnaire_data(name=qname)

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
                col = 0
                for key in item:
                    if isinstance(item[key], list):
                        list_string = ''
                        for value in item[key]:
                            list_string = list_string + str(value) + ', '
                        worksheet.write(row, col, list_string)
                        col += 1
                    else:
                        worksheet.write(row, col, item[key])
                        col += 1
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


