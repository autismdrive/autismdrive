from dataclasses import dataclass

from flask_marshmallow.fields import URLFor


@dataclass
class URLForEndpointMap:
    @staticmethod
    def AdminNote(id_param: str = None):
        return URLFor(
            "api.adminnoteendpoint", values={"admin_note_id": f"<{id_param if id_param else 'admin_note_id'}>"}
        )

    @staticmethod
    def AdminNoteListByResource(id_param: str = None):
        return URLFor(
            "api.adminnotelistbyresourceendpoint",
            values={"resource_id": f"<{id_param if id_param else 'resource_id'}>"},
        )

    @staticmethod
    def AdminNoteListByUser(id_param: str = None):
        return URLFor("api.adminnotelistbyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def AdminNoteList():
        return URLFor("api.adminnotelistendpoint")

    @staticmethod
    def CategoryByEvent(id_param: str = None):
        return URLFor("api.categorybyeventendpoint", values={"event_id": f"<{id_param if id_param else 'event_id'}>"})

    @staticmethod
    def CategoryByLocation(id_param: str = None):
        return URLFor(
            "api.categorybylocationendpoint", values={"location_id": f"<{id_param if id_param else 'location_id'}>"}
        )

    @staticmethod
    def CategoryByResource(id_param: str = None):
        return URLFor(
            "api.categorybyresourceendpoint", values={"resource_id": f"<{id_param if id_param else 'resource_id'}>"}
        )

    @staticmethod
    def CategoryByStudy(id_param: str = None):
        return URLFor("api.categorybystudyendpoint", values={"study_id": f"<{id_param if id_param else 'study_id'}>"})

    @staticmethod
    def Category(id_param: str = None):
        return URLFor("api.categoryendpoint", values={"category_id": f"<{id_param if id_param else 'category_id'}>"})

    @staticmethod
    def CategoryList():
        return URLFor("api.categorylistendpoint")

    @staticmethod
    def CategoryNamesList():
        return URLFor("api.categorynameslistendpoint")

    @staticmethod
    def ChainStep(id_param: str = None):
        return URLFor(
            "api.chainstependpoint", values={"chain_step_id": f"<{id_param if id_param else 'chain_step_id'}>"}
        )

    @staticmethod
    def ChainStepList():
        return URLFor("api.chainsteplistendpoint")

    @staticmethod
    def Config():
        return URLFor("api.configendpoint")

    @staticmethod
    def Covid19ResourceList():
        return URLFor("api.covid19resourcelistendpoint", values={"category": "<category>"})

    @staticmethod
    def DataTransferLog(id_param: str = None):
        return URLFor(
            "api.datatransferlogendpoint",
            values={"data_transfer_log_id": f"<{id_param if id_param else 'data_transfer_log_id'}>"},
        )

    @staticmethod
    def EducationResourceList():
        return URLFor("api.educationresourcelistendpoint")

    @staticmethod
    def EmailLog(id_param: str = None):
        return URLFor("api.emaillogendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def EmailLogList():
        return URLFor("api.emailloglistendpoint")

    @staticmethod
    def EventByCategory(id_param: str = None):
        return URLFor(
            "api.eventbycategoryendpoint", values={"category_id": f"<{id_param if id_param else 'category_id'}>"}
        )

    @staticmethod
    def EventByUser(id_param: str = None):
        return URLFor("api.eventbyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def EventCategory(id_param: str = None):
        return URLFor(
            "api.eventcategoryendpoint",
            values={"event_category_id": f"<{id_param if id_param else 'event_category_id'}>"},
        )

    @staticmethod
    def EventCategoryList():
        return URLFor("api.eventcategorylistendpoint")

    @staticmethod
    def Event(id_param: str = None):
        return URLFor("api.eventendpoint", values={"event_id": f"<{id_param if id_param else 'event_id'}>"})

    @staticmethod
    def EventList():
        return URLFor("api.eventlistendpoint")

    @staticmethod
    def EventUser(id_param: str = None):
        return URLFor(
            "api.eventuserendpoint", values={"event_user_id": f"<{id_param if id_param else 'event_user_id'}>"}
        )

    @staticmethod
    def EventUserList():
        return URLFor("api.eventuserlistendpoint")

    @staticmethod
    def Export():
        return URLFor("api.exportendpoint", values={"name": "<name>"})

    @staticmethod
    def ExportList():
        return URLFor("api.exportlistendpoint")

    @staticmethod
    def FavoritesByUserAndType(id_param: str = None):
        return URLFor(
            "api.favoritesbyuserandtypeendpoint",
            values={"user_id": f"<{id_param if id_param else 'user_id'}>", "favorite_type": "<favorite_type>"},
        )

    @staticmethod
    def FavoritesByUser(id_param: str = None):
        return URLFor("api.favoritesbyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def Flow(id_param: str = None):
        return URLFor(
            "api.flowendpoint",
            values={"name": "<name>", "participant_id": f"<{id_param if id_param else 'participant_id'}>"},
        )

    @staticmethod
    def FlowList():
        return URLFor("api.flowlistendpoint")

    @staticmethod
    def FlowQuestionnaire():
        return URLFor(
            "api.flowquestionnaireendpoint",
            values={"flow_name": "<flow_name>", "questionnaire_name": "<questionnaire_name>"},
        )

    @staticmethod
    def FlowQuestionnaireMeta():
        return URLFor(
            "api.flowquestionnairemetaendpoint",
            values={"flow_name": "<flow_name>", "questionnaire_name": "<questionnaire_name>"},
        )

    @staticmethod
    def InvestigatorByStudy(id_param: str = None):
        return URLFor(
            "api.investigatorbystudyendpoint", values={"study_id": f"<{id_param if id_param else 'study_id'}>"}
        )

    @staticmethod
    def Investigator(id_param: str = None):
        return URLFor(
            "api.investigatorendpoint", values={"investigator_id": f"<{id_param if id_param else 'investigator_id'}>"}
        )

    @staticmethod
    def InvestigatorList():
        return URLFor("api.investigatorlistendpoint")

    @staticmethod
    def LocationByCategory(id_param: str = None):
        return URLFor(
            "api.locationbycategoryendpoint", values={"category_id": f"<{id_param if id_param else 'category_id'}>"}
        )

    @staticmethod
    def LocationCategory(id_param: str = None):
        return URLFor(
            "api.locationcategoryendpoint",
            values={"location_category_id": f"<{id_param if id_param else 'location_category_id'}>"},
        )

    @staticmethod
    def LocationCategoryList():
        return URLFor("api.locationcategorylistendpoint")

    @staticmethod
    def Location(id_param: str = None):
        return URLFor("api.locationendpoint", values={"location_id": f"<{id_param if id_param else 'location_id'}>"})

    @staticmethod
    def LocationList():
        return URLFor("api.locationlistendpoint")

    @staticmethod
    def ParticipantAdminList():
        return URLFor("api.participantadminlistendpoint")

    @staticmethod
    def ParticipantBySession():
        return URLFor("api.participantbysessionendpoint")

    @staticmethod
    def Participant(id_param: str = None):
        return URLFor(
            "api.participantendpoint", values={"participant_id": f"<{id_param if id_param else 'participant_id'}>"}
        )

    @staticmethod
    def ParticipantList():
        return URLFor("api.participantlistendpoint")

    @staticmethod
    def PasswordRequirements():
        return URLFor("api.passwordrequirementsendpoint", values={"role": "<role>"})

    @staticmethod
    def QuestionnaireByParticipant(id_param: str = None):
        return URLFor(
            "api.questionnairebyparticipantendpoint",
            values={"name": "<name>", "participant_id": f"<{id_param if id_param else 'participant_id'}>"},
        )

    @staticmethod
    def QuestionnaireDataExport():
        return URLFor("api.questionnairedataexportendpoint", values={"name": "<name>"})

    @staticmethod
    def Questionnaire(name, id_param: str = None):
        return URLFor(
            "api.questionnaireendpoint",
            values={"name": f"{name}", "questionnaire_id": f"<{id_param if id_param else 'questionnaire_id'}>"},
        )

    @staticmethod
    def QuestionnaireInfo():
        return URLFor("api.questionnaireinfoendpoint")

    @staticmethod
    def QuestionnaireList():
        return URLFor("api.questionnairelistendpoint", values={"name": "<name>"})

    @staticmethod
    def QuestionnaireListMeta():
        return URLFor("api.questionnairelistmetaendpoint", values={"name": "<name>"})

    @staticmethod
    def QuestionnaireUserDataExport(id_param: str = None):
        return URLFor(
            "api.questionnaireuserdataexportendpoint",
            values={"name": "<name>", "user_id": f"<{id_param if id_param else 'user_id'}>"},
        )

    @staticmethod
    def RelatedResults():
        return URLFor("api.relatedresultsendpoint")

    @staticmethod
    def ResourceByCategory(id_param: str = None):
        return URLFor(
            "api.resourcebycategoryendpoint", values={"category_id": f"<{id_param if id_param else 'category_id'}>"}
        )

    @staticmethod
    def ResourceCategory(id_param: str = None):
        return URLFor(
            "api.resourcecategoryendpoint",
            values={"resource_category_id": f"<{id_param if id_param else 'resource_category_id'}>"},
        )

    @staticmethod
    def ResourceCategoryList():
        return URLFor("api.resourcecategorylistendpoint")

    @staticmethod
    def ResourceChangeLogByResource(id_param: str = None):
        return URLFor(
            "api.resourcechangelogbyresourceendpoint",
            values={"resource_id": f"<{id_param if id_param else 'resource_id'}>"},
        )

    @staticmethod
    def ResourceChangeLogByUser(id_param: str = None):
        return URLFor(
            "api.resourcechangelogbyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"}
        )

    @staticmethod
    def Resource(id_param: str = None):
        return URLFor("api.resourceendpoint", values={"resource_id": f"<{id_param if id_param else 'resource_id'}>"})

    @staticmethod
    def ResourceList():
        return URLFor("api.resourcelistendpoint")

    @staticmethod
    def RootCategoryList():
        return URLFor("api.rootcategorylistendpoint")

    @staticmethod
    def Search():
        return URLFor("api.searchendpoint")

    @staticmethod
    def SearchResources():
        return URLFor("api.searchresourcesendpoint")

    @staticmethod
    def SearchStudies():
        return URLFor("api.searchstudiesendpoint")

    @staticmethod
    def Session():
        return URLFor("api.sessionendpoint")

    @staticmethod
    def StepLog(id_param: str = None):
        return URLFor(
            "api.steplogendpoint", values={"participant_id": f"<{id_param if id_param else 'participant_id'}>"}
        )

    @staticmethod
    def StepLogList():
        return URLFor("api.steploglistendpoint")

    @staticmethod
    def StudyByAge():
        return URLFor("api.studybyageendpoint", values={"status": "<status>", "age": "<age>"})

    @staticmethod
    def StudyByCategory(id_param: str = None):
        return URLFor(
            "api.studybycategoryendpoint", values={"category_id": f"<{id_param if id_param else 'category_id'}>"}
        )

    @staticmethod
    def StudyByInvestigator(id_param: str = None):
        return URLFor(
            "api.studybyinvestigatorendpoint",
            values={"investigator_id": f"<{id_param if id_param else 'investigator_id'}>"},
        )

    @staticmethod
    def StudyByStatusList():
        return URLFor("api.studybystatuslistendpoint", values={"status": "<status>"})

    @staticmethod
    def StudyCategory(id_param: str = None):
        return URLFor(
            "api.studycategoryendpoint",
            values={"study_category_id": f"<{id_param if id_param else 'study_category_id'}>"},
        )

    @staticmethod
    def StudyCategoryList():
        return URLFor("api.studycategorylistendpoint")

    @staticmethod
    def Study(id_param: str = None):
        return URLFor("api.studyendpoint", values={"study_id": f"<{id_param if id_param else 'study_id'}>"})

    @staticmethod
    def StudyEnrolledByUser(id_param: str = None):
        return URLFor("api.studyenrolledbyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def StudyInquiryByUser(id_param: str = None):
        return URLFor("api.studyinquirybyuserendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def StudyInquiry():
        return URLFor("api.studyinquiryendpoint")

    @staticmethod
    def StudyInvestigator(id_param: str = None):
        return URLFor(
            "api.studyinvestigatorendpoint",
            values={"study_investigator_id": f"<{id_param if id_param else 'study_investigator_id'}>"},
        )

    @staticmethod
    def StudyInvestigatorList():
        return URLFor("api.studyinvestigatorlistendpoint")

    @staticmethod
    def StudyList():
        return URLFor("api.studylistendpoint")

    @staticmethod
    def StudyUser(id_param: str = None):
        return URLFor(
            "api.studyuserendpoint", values={"study_user_id": f"<{id_param if id_param else 'study_user_id'}>"}
        )

    @staticmethod
    def StudyUserList():
        return URLFor("api.studyuserlistendpoint")

    @staticmethod
    def UserByEvent(id_param: str = None):
        return URLFor("api.userbyeventendpoint", values={"event_id": f"<{id_param if id_param else 'event_id'}>"})

    @staticmethod
    def UserByStudy(id_param: str = None):
        return URLFor("api.userbystudyendpoint", values={"study_id": f"<{id_param if id_param else 'study_id'}>"})

    @staticmethod
    def User(id_param: str = None):
        return URLFor("api.userendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def UserFavorite(id_param: str = None):
        return URLFor(
            "api.userfavoriteendpoint", values={"user_favorite_id": f"<{id_param if id_param else 'user_favorite_id'}>"}
        )

    @staticmethod
    def UserFavoriteList():
        return URLFor("api.userfavoritelistendpoint")

    @staticmethod
    def UserList():
        return URLFor("api.userlistendpoint")

    @staticmethod
    def UserMeta(id_param: str = None):
        return URLFor("api.usermetaendpoint", values={"user_id": f"<{id_param if id_param else 'user_id'}>"})

    @staticmethod
    def UserRegistration():
        return URLFor("api.userregistrationendpoint")

    @staticmethod
    def ZipCodeCoords():
        return URLFor("api.zipcodecoordsendpoint", values={"zip_code": "<zip_code>"})
