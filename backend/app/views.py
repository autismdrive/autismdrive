from app.resources.AdminNoteEndpoint import (
    AdminNoteListByUserEndpoint,
    AdminNoteListByResourceEndpoint,
    AdminNoteListEndpoint,
    AdminNoteEndpoint,
)
from app.resources.CategoryEndpoint import (
    CategoryEndpoint,
    CategoryListEndpoint,
    RootCategoryListEndpoint,
    CategoryNamesListEndpoint,
)
from app.resources.ChainStepEndpoint import ChainStepEndpoint, ChainStepListEndpoint
from app.resources.ConfigEndpoint import ConfigEndpoint
from app.resources.DataTransferLogEndpoint import DataTransferLogEndpoint
from app.resources.EmailLogEndpoint import EmailLogEndpoint, EmailLogListEndpoint
from app.resources.EventAndCategoryEndpoint import (
    EventCategoryEndpoint,
    CategoryByEventEndpoint,
    EventByCategoryEndpoint,
    EventCategoryListEndpoint,
)
from app.resources.EventAndUserEndpoint import (
    EventByUserEndpoint,
    EventUserEndpoint,
    UserByEventEndpoint,
    EventUserListEndpoint,
)
from app.resources.EventEndpoint import EventEndpoint, EventListEndpoint
from app.resources.ExportEndpoint import ExportEndpoint, ExportListEndpoint
from app.resources.FlowEndpoint import (
    FlowEndpoint,
    FlowListEndpoint,
    FlowQuestionnaireEndpoint,
    FlowQuestionnaireMetaEndpoint,
)
from app.resources.InvestigatorEndpoint import InvestigatorEndpoint, InvestigatorListEndpoint
from app.resources.LocationAndCategoryEndpoint import (
    LocationCategoryEndpoint,
    CategoryByLocationEndpoint,
    LocationByCategoryEndpoint,
    LocationCategoryListEndpoint,
)
from app.resources.LocationEndpoint import LocationEndpoint, LocationListEndpoint
from app.resources.ParticipantEndpoint import ParticipantEndpoint, ParticipantListEndpoint, ParticipantAdminListEndpoint
from app.resources.PasswordRequirementsEndpoint import PasswordRequirementsEndpoint
from app.resources.QuestionnaireAndParticipantEndpoint import QuestionnaireByParticipantEndpoint
from app.resources.QuestionnaireEndpoint import (
    QuestionnaireEndpoint,
    QuestionnaireListEndpoint,
    QuestionnaireListMetaEndpoint,
    QuestionnaireDataExportEndpoint,
    QuestionnaireUserDataExportEndpoint,
    QuestionnaireInfoEndpoint,
)
from app.resources.RelatedResultsEndpoint import RelatedResultsEndpoint
from app.resources.ResourceAndCategoryEndpoint import (
    ResourceCategoryEndpoint,
    CategoryByResourceEndpoint,
    ResourceByCategoryEndpoint,
    ResourceCategoryListEndpoint,
)
from app.resources.ResourceChangeLogEndpoint import ResourceChangeLogByUserEndpoint, ResourceChangeLogByResourceEndpoint
from app.resources.ResourceEndpoint import (
    ResourceEndpoint,
    ResourceListEndpoint,
    EducationResourceListEndpoint,
    Covid19ResourceListEndpoint,
)
from app.resources.SearchEndpoint import SearchEndpoint
from app.resources.SearchResourcesEndpoint import SearchResourcesEndpoint
from app.resources.SearchStudiesEndpoint import SearchStudiesEndpoint
from app.resources.SessionEndpoint import SessionEndpoint
from app.resources.StepLogEndpoint import StepLogEndpoint
from app.resources.StepLogEndpoint import StepLogListEndpoint
from app.resources.StudyAndCategoryEndpoint import (
    StudyCategoryEndpoint,
    CategoryByStudyEndpoint,
    StudyByCategoryEndpoint,
    StudyCategoryListEndpoint,
)
from app.resources.StudyAndInvestigatorEndpoint import (
    StudyByInvestigatorEndpoint,
    StudyInvestigatorEndpoint,
    InvestigatorByStudyEndpoint,
    StudyInvestigatorListEndpoint,
)
from app.resources.StudyAndUserEndpoint import (
    StudyInquiryByUserEndpoint,
    StudyEnrolledByUserEndpoint,
    StudyUserEndpoint,
    UserByStudyEndpoint,
    StudyUserListEndpoint,
)
from app.resources.StudyEndpoint import StudyEndpoint, StudyListEndpoint, StudyByStatusListEndpoint, StudyByAgeEndpoint
from app.resources.StudyInquiryEndpoint import StudyInquiryEndpoint
from app.resources.UserAndParticipantEndpoint import ParticipantBySessionEndpoint
from app.resources.UserEndpoint import UserEndpoint, UserListEndpoint, UserRegistrationEndpoint
from app.resources.UserFavoriteEndpoint import (
    UserFavoriteEndpoint,
    UserFavoriteListEndpoint,
    FavoritesByUserEndpoint,
    FavoritesByUserAndTypeEndpoint,
)
from app.resources.UserMetaEndpoint import UserMetaEndpoint
from app.resources.ZipCodeCoordsEndpoint import ZipCodeCoordsEndpoint


endpoints = [
    # Categories
    (CategoryListEndpoint, "/category"),
    (CategoryNamesListEndpoint, "/category/names_list"),
    (RootCategoryListEndpoint, "/category/root"),
    (CategoryEndpoint, "/category/<int:category_id>"),
    (EventByCategoryEndpoint, "/category/<int:category_id>/event"),
    (LocationByCategoryEndpoint, "/category/<int:category_id>/location"),
    (ResourceByCategoryEndpoint, "/category/<int:category_id>/resource"),
    (StudyByCategoryEndpoint, "/category/<int:category_id>/study"),
    # Events
    (EventListEndpoint, "/event"),
    (EventEndpoint, "/event/<int:event_id>"),
    (CategoryByEventEndpoint, "/event/<int:event_id>/category"),
    (EventCategoryListEndpoint, "/event_category"),
    (EventCategoryEndpoint, "/event_category/<int:event_category_id>"),
    (EventByUserEndpoint, "/user/<int:user_id>/event"),
    (UserByEventEndpoint, "/event/<int:event_id>/user"),
    (EventUserEndpoint, "/event_user/<int:event_user_id>"),
    (EventUserListEndpoint, "/event_user"),
    # Locations
    (LocationListEndpoint, "/location"),
    (LocationEndpoint, "/location/<int:location_id>"),
    (CategoryByLocationEndpoint, "/location/<int:location_id>/category"),
    (LocationCategoryListEndpoint, "/location_category"),
    (LocationCategoryEndpoint, "/location_category/<int:location_category_id>"),
    # Resources
    (ResourceListEndpoint, "/resource"),
    (ResourceEndpoint, "/resource/<int:resource_id>"),
    (EducationResourceListEndpoint, "/resource/education"),
    (Covid19ResourceListEndpoint, "/resource/covid19/<string:category>"),
    (CategoryByResourceEndpoint, "/resource/<int:resource_id>/category"),
    (ResourceCategoryListEndpoint, "/resource_category"),
    (ResourceCategoryEndpoint, "/resource_category/<int:resource_category_id>"),
    (ResourceChangeLogByResourceEndpoint, "/resource/<int:resource_id>/change_log"),
    (AdminNoteListByResourceEndpoint, "/resource/<int:resource_id>/admin_note"),
    # Studies
    (StudyListEndpoint, "/study"),
    (StudyByStatusListEndpoint, "/study/status/<string:status>"),
    (StudyByAgeEndpoint, "/study/status/<string:status>/<string:age>"),
    (StudyEndpoint, "/study/<int:study_id>"),
    (CategoryByStudyEndpoint, "/study/<int:study_id>/category"),
    (StudyCategoryListEndpoint, "/study_category"),
    (StudyCategoryEndpoint, "/study_category/<int:study_category_id>"),
    (InvestigatorByStudyEndpoint, "/study/<int:study_id>/investigator"),
    (StudyInvestigatorListEndpoint, "/study_investigator"),
    (StudyInvestigatorEndpoint, "/study_investigator/<int:study_investigator_id>"),
    (UserByStudyEndpoint, "/study/<int:study_id>/user"),
    (StudyUserListEndpoint, "/study_user"),
    (StudyUserEndpoint, "/study_user/<int:study_user_id>"),
    (StudyInquiryEndpoint, "/study_inquiry"),
    # Investigators
    (InvestigatorListEndpoint, "/investigator"),
    (InvestigatorEndpoint, "/investigator/<int:investigator_id>"),
    (StudyByInvestigatorEndpoint, "/investigator/<int:investigator_id>/study"),
    # User Sessions
    (SessionEndpoint, "/session"),
    (ParticipantBySessionEndpoint, "/session/participant"),
    # User Schema, Admin endpoints
    (UserListEndpoint, "/user"),
    (UserRegistrationEndpoint, "/user/registration"),
    (UserEndpoint, "/user/<int:user_id>"),
    (StudyInquiryByUserEndpoint, "/user/<int:user_id>/inquiry/study"),
    (StudyEnrolledByUserEndpoint, "/user/<int:user_id>/enrolled/study"),
    (FavoritesByUserEndpoint, "/user/<int:user_id>/favorite"),
    (FavoritesByUserAndTypeEndpoint, "/user/<int:user_id>/favorite/<string:favorite_type>"),
    (UserFavoriteListEndpoint, "/user_favorite"),
    (UserFavoriteEndpoint, "/user_favorite/<int:user_favorite_id>"),
    (EmailLogEndpoint, "/user/email_log/<int:user_id>"),
    (ResourceChangeLogByUserEndpoint, "/user/<int:user_id>/resource_change_log"),
    (AdminNoteListByUserEndpoint, "/user/<int:user_id>/admin_note"),
    (UserMetaEndpoint, "/user/<int:user_id>/usermeta"),
    # Participants
    (ParticipantListEndpoint, "/participant"),
    (ParticipantEndpoint, "/participant/<int:participant_id>"),
    (ParticipantAdminListEndpoint, "/participant_admin_list"),
    (StepLogEndpoint, "/participant/step_log/<int:participant_id>"),
    # Questionnaires
    (QuestionnaireInfoEndpoint, "/q"),
    (QuestionnaireListEndpoint, "/q/<string:name>"),
    (QuestionnaireByParticipantEndpoint, "/q/<string:name>/participant/<int:participant_id>"),
    (QuestionnaireListMetaEndpoint, "/q/<string:name>/meta"),
    (QuestionnaireEndpoint, "/q/<string:name>/<int:questionnaire_id>"),
    (QuestionnaireDataExportEndpoint, "/q/<string:name>/export"),
    (QuestionnaireUserDataExportEndpoint, "/q/<string:name>/export/user/<int:user_id>"),
    # Flows
    (FlowEndpoint, "/flow/<string:name>/<int:participant_id>"),
    (FlowListEndpoint, "/flow"),
    (FlowQuestionnaireEndpoint, "/flow/<string:flow_name>/<string:questionnaire_name>"),
    (FlowQuestionnaireMetaEndpoint, "/flow/<string:flow_name>/<string:questionnaire_name>/meta"),
    # Search
    (SearchEndpoint, "/search"),
    (SearchResourcesEndpoint, "/search/resources"),
    (SearchStudiesEndpoint, "/search/studies"),
    (RelatedResultsEndpoint, "/related"),
    # Admin
    (ExportListEndpoint, "/export"),
    (ExportEndpoint, "/export/<string:name>"),
    (EmailLogListEndpoint, "/email_log"),
    (StepLogListEndpoint, "/step_log"),
    (AdminNoteListEndpoint, "/admin_note"),
    (AdminNoteEndpoint, "/admin_note/<int:admin_note_id>"),
    (ConfigEndpoint, "/config"),
    (DataTransferLogEndpoint, "/data_transfer_log"),
    # ZIP Code Endpoint
    (ZipCodeCoordsEndpoint, "/zip_code_coords/<int:zip_code>"),
    # Password Requirements Endpoint
    (PasswordRequirementsEndpoint, "/password_requirements/<string:role>"),
    # SkillSTAR
    (ChainStepListEndpoint, "/chain_step"),
    (ChainStepEndpoint, "/chain_step/<int:chain_step_id>"),
]
