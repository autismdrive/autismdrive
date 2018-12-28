import sys
from flask import json
from app.model.category import Category
from app.model.email_log import EmailLog
from app.model.organization import Organization
from app.model.resource import StarResource
from app.model.resource_category import ResourceCategory
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.training import Training
from app.model.training_category import TrainingCategory
from app.model.user import User
from app import db
import csv


class DataLoader():
    "Loads CSV files into the database"
    file = "example_data/resources.csv"

    def __init__(self, directory="./example_data"):
        self.category_file = directory + "/categories.csv"
        self.resource_file = directory + "/resources.csv"
        self.study_file = directory + "/studies.csv"
        self.training_file = directory + "/trainings.csv"
        self.user_file = directory + "/users.csv"
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

                for i in range(14, 19):
                    if not row[i]: continue
                    category = self.get_category_by_name(row[i])
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
                user = User(id=row[0], email=row[1], first_name=row[2], last_name=row[3], password=row[4],
                            role=row[5], email_verified=True)
                db.session.add(user)
            print("Users loaded.  There are now %i users in the database." % db.session.query(
                User).count())
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
        db.session.query(ResourceCategory).delete()
        db.session.query(StudyCategory).delete()
        db.session.query(TrainingCategory).delete()
        db.session.query(Category).delete()
        db.session.query(EmailLog).delete()
        db.session.query(StarResource).delete()
        db.session.query(Study).delete()
        db.session.query(Training).delete()
        db.session.query(User).delete()
        db.session.commit()
