import sys
from flask import json
from app.model.category import Category
from app.model.email_log import EmailLog
from app.model.organization import Organization
from app.model.participant import Participant
from app.model.resource import StarResource
from app.model.resource_category import ResourceCategory
from app.model.step_log import StepLog
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.training import Training
from app.model.training_category import TrainingCategory
from app.model.user import User
from app.model.questionnaires.clinical_diagnoses_dependent_questionnaire import ClinicalDiagnosesDependentQuestionnaire
from app.model.questionnaires.clinical_diagnoses_self_questionnaire import ClinicalDiagnosesSelfQuestionnaire
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire
from app.model.questionnaires.current_behaviors_questionnaire import CurrentBehaviorsQuestionnaire
from app.model.questionnaires.demographics_questionnaire import DemographicsQuestionnaire
from app.model.questionnaires.developmental_questionnaire import DevelopmentalQuestionnaire
from app.model.questionnaires.education_questionnaire import EducationQuestionnaire
from app.model.questionnaires.employment_questionnaire import EmploymentQuestionnaire
from app.model.questionnaires.evaluation_history_questionnaire import EvaluationHistoryQuestionnaire
from app.model.questionnaires.home_questionnaire import HomeQuestionnaire
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire
from app.model.questionnaires.supports_questionnaire import SupportsQuestionnaire
from app import db
from sqlalchemy import Sequence
import csv

from app.model.user_participant import UserParticipant


class DataLoader():
    "Loads CSV files into the database"
    file = "example_data/resources.csv"

    def __init__(self, directory="./example_data"):
        self.category_file = directory + "/categories.csv"
        self.resource_file = directory + "/resources.csv"
        self.study_file = directory + "/studies.csv"
        self.training_file = directory + "/trainings.csv"
        self.user_file = directory + "/users.csv"
        self.participant_file = directory + "/participants.csv"
        self.user_participant_file = directory + "/user_participants.csv"
        print("Data loader initialized")

    def load_categories(self):
        with open(self.category_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                parent = self.get_category_by_name(row[1]) if row[1] else None
                category = Category(name=row[0], parent=parent)
                db.session.add(category)
            print("Categories loaded.  There are now %i categories in the database." % db.session.query(
                Category).count())
        db.session.commit()

    def load_resources(self):
        with open(self.resource_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[5]) if row[5] else None
                resource = StarResource(id=row[0], title=row[1], description=row[2], image_url=row[3], image_caption=row[4],
                                        organization=org, street_address1=row[6], street_address2=row[7], city=row[8],
                                        state=row[9], zip=row[10], county=row[11], website=row[12], phone=row[13])
                db.session.add(resource)
                self.__increment_id_sequence(StarResource)

                for i in range(14, 19):
                    if not row[i]: continue
                    category = self.get_category_by_name(row[i].strip())
                    resource_id = eval(row[0])
                    category_id = category.id

                    resource_category = ResourceCategory(resource_id=resource_id, category_id=category_id)
                    db.session.add(resource_category)
            print("Resources loaded.  There are now %i resources in the database." % db.session.query(
                StarResource).count())
            print("There are now %i links between resources and categories in the database." %
                  db.session.query(ResourceCategory).count())
        db.session.commit()

    def load_studies(self):
        with open(self.study_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[12]) if row[12] else None
                study = Study(id=row[0], title=row[1], description=row[2], researcher_description=row[3],
                              participant_description=row[4], outcomes_description=row[5], enrollment_start_date=row[6],
                              enrollment_end_date=row[7], current_num_participants=row[8], max_num_participants=row[9],
                              start_date=row[10], end_date=row[11], organization=org)
                db.session.add(study)
                self.__increment_id_sequence(Study)

                for i in range(13, 17):
                    if not row[i]: continue
                    category = self.get_category_by_name(row[i])
                    study_id = eval(row[0])
                    category_id = category.id

                    study_category = StudyCategory(study_id=study_id, category_id=category_id)
                    db.session.add(study_category)
            print("Studies loaded.  There are now %i studies in the database." % db.session.query(
                Study).count())
            print("There are now %i links between studies and categories in the database." %
                  db.session.query(StudyCategory).count())
        db.session.commit()

    def load_trainings(self):
        with open(self.training_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[6]) if row[6] else None
                training = Training(id=row[0], title=row[1], description=row[2], outcomes_description=row[3], image_url=row[4],
                                    image_caption=row[5], organization=org, website=row[7])
                db.session.add(training)
                self.__increment_id_sequence(Training)

                for i in range(8, 12):
                    if not row[i]: continue
                    category = self.get_category_by_name(row[i])
                    training_id = eval(row[0])
                    category_id = category.id

                    training_category = TrainingCategory(training_id=training_id, category_id=category_id)
                    db.session.add(training_category)
            print("Trainings loaded.  There are now %i trainings in the database." % db.session.query(
                Training).count())
            print("There are now %i links between trainings and categories in the database." %
                  db.session.query(TrainingCategory).count())
        db.session.commit()

    def load_users(self):
        with open(self.user_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                user = User(id=row[0], email=row[1], password=row[2],
                            role=row[3], email_verified=True)
                db.session.add(user)
                self.__increment_id_sequence(User)
            print("Users loaded.  There are now %i users in the database." % db.session.query(
                User).count())
        db.session.commit()

    def load_participants(self):
        with open(self.participant_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                participant = Participant(id=row[0], first_name=row[1], last_name=row[2])
                db.session.add(participant)
                self.__increment_id_sequence(Participant)
            print("Participants loaded.  There are now %i participants in the database." % db.session.query(
                Participant).count())
        db.session.commit()

    def link_users_participants(self):
        with open(self.user_participant_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                user_particpant = UserParticipant(id=row[0], participant_id=row[1],
                                                  user_id=row[2], relationship=row[3])
                db.session.add(user_particpant)
                self.__increment_id_sequence(UserParticipant)
            print("Participants/Users linked.  There are now %i relationships in the database." % db.session.query(
                UserParticipant).count())
        db.session.commit()

    def load_clinical_diagnoses_questionnaires(self):
        cd_dques = ClinicalDiagnosesDependentQuestionnaire(mental_health='ptsd', genetic='angelman')
        db.session.add(cd_dques)
        print("Clinical Diagnoses for Dependents loaded. There is now %i dependent clinical diagnoses record in the database." % db.session.query(
            ClinicalDiagnosesDependentQuestionnaire).count())
        cd_sques = ClinicalDiagnosesSelfQuestionnaire(mental_health='ptsd', genetic='angelman')
        db.session.add(cd_sques)
        print("Clinical Diagnoses for Self users loaded. There is now %i self clinical diagnoses record in the database." % db.session.query(
            ClinicalDiagnosesSelfQuestionnaire).count())
        db.session.commit()

    def load_contact_questionnaire(self):
        c_ques = ContactQuestionnaire(phone=555-555-1234, contact_times='Weekdays at 5AM', email='charlie@brown.com')
        db.session.add(c_ques)
        print("Contact loaded.  There is now %i contact record in the database." % db.session.query(
            ContactQuestionnaire).count())
        db.session.commit()

    def load_current_behaviors_questionnaire(self):
        cb_ques = CurrentBehaviorsQuestionnaire(self_verbal_ability='nonVerbal', has_academic_difficulties=True)
        db.session.add(cb_ques)
        print("Current Behaviors loaded.  There is now %i current behavior record in the database." % db.session.query(
            CurrentBehaviorsQuestionnaire).count())
        db.session.commit()

    def load_demographics_questionnaire(self):
        d_ques = DemographicsQuestionnaire(user_id=1, birth_sex='male', gender_identity='intersex',
                                           race_ethnicity="raceAsian")
        db.session.add(d_ques)
        print("Demographics loaded.  There is now %i demographics record in the database." % db.session.query(
            DemographicsQuestionnaire).count())
        db.session.commit()

    def load_developmental_questionnaire(self):
        d_ques = DevelopmentalQuestionnaire(had_birth_complications=True, when_language_milestones="early")
        db.session.add(d_ques)
        print("Developmental History loaded.  There is now %i developmental record in the database." % db.session.query(
            DevelopmentalQuestionnaire).count())
        db.session.commit()

    def load_education_questionnaire(self):
        e_ques = EducationQuestionnaire(attends_school=True, school_name="Staunton Montessori School")
        db.session.add(e_ques)
        print("Education loaded.  There is now %i education record in the database." % db.session.query(
            EducationQuestionnaire).count())
        db.session.commit()

    def load_employment_questionnaire(self):
        em_ques = EmploymentQuestionnaire(is_currently_employed=True, employment_capacity='fullTime', has_employment_support=False)
        db.session.add(em_ques)
        print("Employment loaded.  There is now %i employment record in the database." % db.session.query(
            EmploymentQuestionnaire).count())
        db.session.commit()

    def load_evaluation_history_questionnaire(self):
        eh_ques = EvaluationHistoryQuestionnaire(self_identifies_autistic=True, years_old_at_first_diagnosis=10, where_diagnosed="uva")
        db.session.add(eh_ques)
        print("Evaluation History loaded.  There is now %i evaluation history record in the database." % db.session.query(
            EvaluationHistoryQuestionnaire).count())
        db.session.commit()

    def load_home_questionnaire(self):
        h_ques = HomeQuestionnaire(self_living_situation="spouse", struggle_to_afford=True)
        db.session.add(h_ques)
        print("Home loaded.  There is now %i home record in the database." % db.session.query(
            HomeQuestionnaire).count())
        db.session.commit()

    def load_identification_questionnaire(self):
        i_ques = IdentificationQuestionnaire(first_name="Charles", middle_name="Monroe", last_name="Brown",
                                             is_first_name_preferred=False, nickname="Charlie", birthdate="1979-1-5",
                                             birth_city="Staunton", birth_state="VA", is_english_primary=True)
        db.session.add(i_ques)
        print("Identification loaded.  There is now %i home record in the database." % db.session.query(
            IdentificationQuestionnaire).count())
        db.session.commit()

    def load_supports_questionnaire(self):
        s_ques = SupportsQuestionnaire()
        db.session.add(s_ques)
        print("Supports loaded.  There is now %i supports record in the database." % db.session.query(
            SupportsQuestionnaire).count())
        db.session.commit()

    def get_org_by_name(self, org_name):
        organization = db.session.query(Organization).filter(Organization.name == org_name).first()
        if organization is None:
            organization = Organization(name=org_name)
            db.session.add(organization)
            db.session.commit()
        return organization

    def get_category_by_name(self, category_name):
        category = db.session.query(Category).filter(Category.name == category_name).first()
        if category is None:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
        return category

    def clear(self):
        db.session.query(ClinicalDiagnosesDependentQuestionnaire).delete()
        db.session.query(ClinicalDiagnosesSelfQuestionnaire).delete()
        db.session.query(ContactQuestionnaire).delete()
        db.session.query(CurrentBehaviorsQuestionnaire).delete()
        db.session.query(DemographicsQuestionnaire).delete()
        db.session.query(DevelopmentalQuestionnaire).delete()
        db.session.query(EducationQuestionnaire).delete()
        db.session.query(EmploymentQuestionnaire).delete()
        db.session.query(EvaluationHistoryQuestionnaire).delete()
        db.session.query(HomeQuestionnaire).delete()
        db.session.query(IdentificationQuestionnaire).delete()
        db.session.query(SupportsQuestionnaire).delete()
        db.session.query(StepLog).delete()
        db.session.query(ResourceCategory).delete()
        db.session.query(StudyCategory).delete()
        db.session.query(TrainingCategory).delete()
        db.session.query(Category).delete()
        db.session.query(EmailLog).delete()
        db.session.query(StarResource).delete()
        db.session.query(Study).delete()
        db.session.query(Training).delete()
        db.session.query(UserParticipant).delete()
        db.session.query(Participant).delete()
        db.session.query(User).delete()
        db.session.commit()

    def __increment_id_sequence(self, model):
        db.session.execute(Sequence(model.__tablename__ + '_id_seq'))
