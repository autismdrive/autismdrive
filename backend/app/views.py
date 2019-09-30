import urllib

import flask_restful
from flask import Blueprint, jsonify, url_for
from flask_restful import reqparse

from app import app
from app.resources.ConfigEndpoint import ConfigEndpoint
from app.resources.RelatedResultsEndpoint import RelatedResultsEndpoint
from app.resources.Auth import auth_blueprint
from app.resources.EmailLogEndpoint import EmailLogListEndpoint
from app.resources.SearchEndpoint import SearchEndpoint
from app.resources.SearchResourcesEndpoint import SearchResourcesEndpoint
from app.resources.SearchStudiesEndpoint import SearchStudiesEndpoint
from app.resources.StepLogEndpoint import StepLogListEndpoint
from app.resources.Tracking import tracking_blueprint
from app.resources.FlowEndpoint import (
    FlowEndpoint,
    FlowListEndpoint,
    FlowQuestionnaireEndpoint,
    FlowQuestionnaireMetaEndpoint)
from app.resources.UserEndpoint import UserEndpoint, UserListEndpoint
from app.resources.EmailLogEndpoint import EmailLogEndpoint
from app.resources.StepLogEndpoint import StepLogEndpoint
from app.resources.AdminNoteEndpoint import (
    AdminNoteListByUserEndpoint,
    AdminNoteListByResourceEndpoint,
    AdminNoteListEndpoint,
    AdminNoteEndpoint)
from app.resources.StudyEndpoint import StudyEndpoint, StudyListEndpoint
from app.resources.InvestigatorEndpoint import InvestigatorEndpoint, InvestigatorListEndpoint
from app.resources.SessionEndpoint import SessionEndpoint
from app.resources.CategoryEndpoint import (
    CategoryEndpoint,
    CategoryListEndpoint,
    RootCategoryListEndpoint
)
from app.resources.EventEndpoint import (
    EventEndpoint,
    EventListEndpoint
)
from app.resources.LocationEndpoint import (
    LocationEndpoint,
    LocationListEndpoint
)
from app.resources.ResourceEndpoint import (
    ResourceEndpoint,
    ResourceListEndpoint
)
from app.resources.ParticipantEndpoint import ParticipantEndpoint, ParticipantListEndpoint
from app.resources.OrganizationEndpoint import (
    OrganizationEndpoint,
    OrganizationListEndpoint
)
from app.resources.QuestionnaireAndParticipantEndpoint import QuestionnaireByParticipantEndpoint
from app.resources.QuestionnaireEndpoint import (
    QuestionnaireEndpoint,
    QuestionnaireListEndpoint,
    QuestionnaireListMetaEndpoint,
    QuestionnaireDataExportEndpoint,
    QuestionnaireUserDataExportEndpoint,
    QuestionnaireInfoEndpoint)
from app.resources.SessionStatusEndpoint import SessionStatusEndpoint
from app.resources.StudyAndCategoryEndpoint import (
    StudyCategoryEndpoint,
    CategoryByStudyEndpoint,
    StudyByCategoryEndpoint,
    StudyCategoryListEndpoint
)
from app.resources.StudyAndInvestigatorEndpoint import (
    StudyByInvestigatorEndpoint,
    StudyInvestigatorEndpoint,
    InvestigatorByStudyEndpoint,
    StudyInvestigatorListEndpoint
)
from app.resources.StudyAndUserEndpoint import (
    StudyByUserEndpoint,
    StudyInquiryByUserEndpoint,
    StudyEnrolledByUserEndpoint,
    StudyUserEndpoint,
    UserByStudyEndpoint,
    StudyUserListEndpoint
)
from app.resources.StudyInquiryEndpoint import (
    StudyInquiryEndpoint
)
from app.resources.UserAndParticipantEndpoint import (
    ParticipantBySessionEndpoint
)
from app.resources.EventAndCategoryEndpoint import (
    EventCategoryEndpoint,
    CategoryByEventEndpoint,
    EventByCategoryEndpoint,
    EventCategoryListEndpoint
)
from app.resources.LocationAndCategoryEndpoint import (
    LocationCategoryEndpoint,
    CategoryByLocationEndpoint,
    LocationByCategoryEndpoint,
    LocationCategoryListEndpoint
)
from app.resources.ResourceAndCategoryEndpoint import (
    ResourceCategoryEndpoint,
    CategoryByResourceEndpoint,
    ResourceByCategoryEndpoint,
    ResourceCategoryListEndpoint
)
from app.resources.ExportEndpoint import (
    ExportEndpoint,
    ExportListEndpoint
)
from app.resources.DataTransferLogEndpoint import DataTransferLogEndpoint
from app.resources.ZipCodeCoordsEndpoint import ZipCodeCoordsEndpoint


class StarDriveApi(flask_restful.Api):
    # Define a custom error handler for all rest endpoints that
    # properly handles the RestException status.
    def handle_error(self, e):
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        flask_restful.abort(e.status_code, response)


api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = StarDriveApi(api_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(tracking_blueprint)

parser = flask_restful.reqparse.RequestParser()
parser.add_argument("resource")


@app.route("/", methods=["GET"])
def root():
    output = {}
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "<{0}>".format(arg)

        methods = ",".join(rule.methods)
        url = url_for(rule.endpoint, **options)
        output[rule.endpoint] = urllib.parse.unquote(url)

    return jsonify(output)


endpoints = [
    # Categories
    (CategoryListEndpoint, "/category"),
    (RootCategoryListEndpoint, "/category/root"),
    (CategoryEndpoint, "/category/<id>"),
    (EventByCategoryEndpoint, "/category/<category_id>/event"),
    (LocationByCategoryEndpoint, "/category/<category_id>/location"),
    (ResourceByCategoryEndpoint, "/category/<category_id>/resource"),
    (StudyByCategoryEndpoint, "/category/<category_id>/study"),
    # Organizations
    (OrganizationListEndpoint, "/organization"),
    (OrganizationEndpoint, "/organization/<id>"),
    # Events
    (EventListEndpoint, "/event"),
    (EventEndpoint, "/event/<id>"),
    (CategoryByEventEndpoint, "/event/<event_id>/category"),
    (EventCategoryListEndpoint, "/event_category"),
    (EventCategoryEndpoint, "/event_category/<id>"),
    # Locations
    (LocationListEndpoint, "/location"),
    (LocationEndpoint, "/location/<id>"),
    (CategoryByLocationEndpoint, "/location/<location_id>/category"),
    (LocationCategoryListEndpoint, "/location_category"),
    (LocationCategoryEndpoint, "/location_category/<id>"),
    # Resources
    (ResourceListEndpoint, "/resource"),
    (ResourceEndpoint, "/resource/<id>"),
    (CategoryByResourceEndpoint, "/resource/<resource_id>/category"),
    (ResourceCategoryListEndpoint, "/resource_category"),
    (ResourceCategoryEndpoint, "/resource_category/<id>"),
    (AdminNoteListByResourceEndpoint, "/resource/<resource_id>/admin_note"),

    # Studies
    (StudyListEndpoint, "/study"),
    (StudyEndpoint, "/study/<id>"),
    (CategoryByStudyEndpoint, "/study/<study_id>/category"),
    (StudyCategoryListEndpoint, "/study_category"),
    (StudyCategoryEndpoint, "/study_category/<id>"),
    (InvestigatorByStudyEndpoint, "/study/<study_id>/investigator"),
    (StudyInvestigatorListEndpoint, "/study_investigator"),
    (StudyInvestigatorEndpoint, "/study_investigator/<id>"),
    (UserByStudyEndpoint, "/study/<study_id>/user"),
    (StudyUserListEndpoint, "/study_user"),
    (StudyUserEndpoint, "/study_user/<id>"),
    (StudyInquiryEndpoint, "/study_inquiry"),

    # Investigators
    (InvestigatorListEndpoint, "/investigator"),
    (InvestigatorEndpoint, "/investigator/<id>"),
    (StudyByInvestigatorEndpoint, "/investigator/<investigator_id>/study"),

    # User Sessions
    (SessionEndpoint, "/session"),
    (ParticipantBySessionEndpoint, "/session/participant"),

    # User Schema, Admin endpoints
    (UserListEndpoint, "/user"),
    (UserEndpoint, "/user/<id>"),
    (StudyByUserEndpoint, "/user/<user_id>/study"),
    (StudyInquiryByUserEndpoint, "/user/<user_id>/inquiry/study"),
    (StudyEnrolledByUserEndpoint, "/user/<user_id>/enrolled/study"),
    (EmailLogEndpoint, "/user/email_log/<user_id>"),
    (AdminNoteListByUserEndpoint, "/user/<user_id>/admin_note"),
    # Participants
    (ParticipantListEndpoint, "/participant"),
    (ParticipantEndpoint, "/participant/<id>"),
    (StepLogEndpoint, "/participant/step_log/<participant_id>"),
    # Questionnaires
    (QuestionnaireInfoEndpoint, "/q"),
    (QuestionnaireListEndpoint, "/q/<string:name>"),
    (QuestionnaireByParticipantEndpoint, "/q/<string:name>/participant/<string:participant_id>"),
    (QuestionnaireListMetaEndpoint, "/q/<string:name>/meta"),
    (QuestionnaireEndpoint, "/q/<string:name>/<string:id>"),
    (QuestionnaireDataExportEndpoint, "/q/<string:name>/export"),
    (QuestionnaireUserDataExportEndpoint, "/q/<string:name>/export/user/<string:user_id>"),
    # Flow Endpoint
    (FlowEndpoint, "/flow/<string:name>/<string:participant_id>"),
    (FlowListEndpoint, "/flow"),
    (FlowQuestionnaireEndpoint, "/flow/<string:flow>/<string:questionnaire_name>"),
    (FlowQuestionnaireMetaEndpoint, "/flow/<string:flow>/<string:questionnaire_name>/meta"),
    # Search Endpoint
    (SearchEndpoint, "/search"),
    (SearchResourcesEndpoint, "/search/resources"),
    (SearchStudiesEndpoint, "/search/studies"),
    (RelatedResultsEndpoint, "/related"),

    (ExportListEndpoint, "/export"),
    (ExportEndpoint, "/export/<string:name>"),
    (EmailLogListEndpoint, "/email_log"),
    (StepLogListEndpoint, "/step_log"),
    (AdminNoteListEndpoint, "/admin_note"),
    (AdminNoteEndpoint, "/admin_note/<string:id>"),
    (ConfigEndpoint, "/config"),
    (DataTransferLogEndpoint, "/data_transfer_log"),

    # ZIP Code Endpoint
    (ZipCodeCoordsEndpoint, "/zip_code_coords/<id>"),

]

# Add all endpoints to the API
for endpoint in endpoints:
    api.add_resource(endpoint[0], endpoint[1])
