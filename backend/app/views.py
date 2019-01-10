from flask import jsonify, url_for, Blueprint
from app import app
import flask_restful
from flask_restful import reqparse

from app.resources.Auth import auth_blueprint
from app.resources.CategoryEndpoint import CategoryEndpoint, CategoryListEndpoint, RootCategoryListEndpoint
from app.resources.ContactQuestionnaireEndpoint import ContactQuestionnaireEndpoint, ContactQuestionnaireListEndpoint, ContactQuestionnaireMetaEndpoint
from app.resources.OrganizationEndpoint import OrganizationListEndpoint, OrganizationEndpoint
from app.resources.ResourceAndCategoryEndpoint import ResourceCategoryEndpoint, ResourceCategoryListEndpoint, \
    ResourceByCategoryEndpoint, CategoryByResourceEndpoint
from app.resources.StudyAndCategoryEndpoint import StudyCategoryEndpoint, StudyCategoryListEndpoint, \
    StudyByCategoryEndpoint, CategoryByStudyEndpoint
from app.resources.TrainingAndCategoryEndpoint import TrainingCategoryEndpoint, TrainingCategoryListEndpoint, \
    TrainingByCategoryEndpoint, CategoryByTrainingEndpoint
from app.resources.ResourceEndpoint import ResourceListEndpoint, ResourceEndpoint
from app.resources.SessionEndpoint import SessionEndpoint
from app.resources.StudyEndpoint import StudyListEndpoint, StudyEndpoint
from app.resources.Tracking import tracking_blueprint
from app.resources.TrainingEndpoint import TrainingListEndpoint, TrainingEndpoint
from app.resources.UserEndpoint import UserListEndpoint, UserEndpoint


class StarDriveApi(flask_restful.Api):
    # Define a custom error handler for all rest endpoints that
    # properly handles the RestException status.
    def handle_error(self, e):
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        flask_restful.abort(e.status_code, response)


api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = StarDriveApi(api_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(tracking_blueprint)


parser = flask_restful.reqparse.RequestParser()
parser.add_argument('resource')


@app.route('/', methods=['GET'])
def root():
    _links = {"_links": {
        "resources": url_for("api.resourcelistendpoint"),
        "studies": url_for("api.studylistendpoint"),
        "trainings": url_for("api.traininglistendpoint"),
        "categories": url_for("api.categorylistendpoint"),
        "organizations": url_for("api.organizationlistendpoint"),
        "users": url_for("api.userlistendpoint"),
        "auth": url_for("auth.login_password"),
    }}
    return jsonify(_links)


api.add_resource(CategoryListEndpoint, '/category')
api.add_resource(CategoryEndpoint, '/category/<id>')
api.add_resource(RootCategoryListEndpoint, '/category/root')
api.add_resource(ContactQuestionnaireListEndpoint, '/contact_questionnaire')
api.add_resource(ContactQuestionnaireEndpoint, '/contact_questionnaire/<id>')
api.add_resource(ContactQuestionnaireMetaEndpoint, '/contact_questionnaire/meta')
api.add_resource(ResourceByCategoryEndpoint, '/category/<category_id>/resource')
api.add_resource(StudyByCategoryEndpoint, '/category/<category_id>/study')
api.add_resource(TrainingByCategoryEndpoint, '/category/<category_id>/training')
api.add_resource(OrganizationListEndpoint, '/organization')
api.add_resource(OrganizationEndpoint, '/organization/<id>')
api.add_resource(ResourceListEndpoint, '/resource')
api.add_resource(ResourceEndpoint, '/resource/<id>')
api.add_resource(CategoryByResourceEndpoint, '/resource/<resource_id>/category')
api.add_resource(StudyListEndpoint, '/study')
api.add_resource(StudyEndpoint, '/study/<id>')
api.add_resource(CategoryByStudyEndpoint, '/study/<study_id>/category')
api.add_resource(TrainingListEndpoint, '/training')
api.add_resource(TrainingEndpoint, '/training/<id>')
api.add_resource(CategoryByTrainingEndpoint, '/training/<training_id>/category')
api.add_resource(ResourceCategoryListEndpoint, '/resource_category')
api.add_resource(ResourceCategoryEndpoint, '/resource_category/<id>')
api.add_resource(StudyCategoryListEndpoint, '/study_category')
api.add_resource(StudyCategoryEndpoint, '/study_category/<id>')
api.add_resource(TrainingCategoryListEndpoint, '/training_category')
api.add_resource(TrainingCategoryEndpoint, '/training_category/<id>')
api.add_resource(UserListEndpoint, '/user')
api.add_resource(UserEndpoint, '/user/<id>')
api.add_resource(SessionEndpoint, '/session')
