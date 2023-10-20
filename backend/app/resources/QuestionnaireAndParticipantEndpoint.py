import flask_restful

from app.auth import auth
from app.database import session, get_class
from app.enums import Permission
from app.export_service import ExportService
from app.wrappers import requires_permission


# The Questionnaire by Participant Endpoint expects a "type" that is the exact Class name of a file
# located in the Questionnaire Package. It should have the following properties:
#   * It is saved in a snaked cased file of the same name as the class.
#   * It extends db.Model
#   * it has an id field called "id"
#   * It has a date field called "last_updated"
#   * When calling the endpoint, use the snakecase format of the name.


class QuestionnaireByParticipantEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, name, participant_id):
        class_ref = get_class(name)
        schema = ExportService.get_schema(name, many=True)
        questionnaires = session.query(class_ref).filter(class_ref.participant_id == participant_id).all()
        return schema.dump(questionnaires)
