import sys
from flask import json
from app.model.email_log import EmailLog
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.user import User
from app import db
import csv


class DataLoader():
    "Loads CSV files into the database"
    file = "example_data/resources.csv"

    def __init__(self, directory="./example_data"):
        self.resource_file = directory + "/resources.csv"
        self.study_file = directory + "/studies.csv"
        self.training_file = directory + "/trainings.csv"
        self.user_file = directory + "/users.csv"
        print("Data loader initialized")

    def load_resources(self):
        with open(self.resource_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                resource = StarResource(id=row[0], title=row[1], description=row[2], image=row[3], image_caption=row[4],
                                        organization=row[5], street_address1=row[6], street_address2=row[7],
                                        city=row[8], state=row[9], zip=row[10], county=row[11], website=row[12],
                                        phone=row[13])
                db.session.add(resource)
            print("Resources loaded.  There are now %i resources in the database." % db.session.query(
                StarResource).count())
        db.session.commit()

    def load_studies(self):
        with open(self.study_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:

                study = Study(id=row[0], title=row[1], description=row[2], researcher_description=row[3],
                              participant_description=row[4], outcomes=row[5], enrollment_date=row[6],
                              current_enrolled=row[7], total_participants=row[8], study_start=row[9], study_end=row[10])
                db.session.add(study)
            print("Studies loaded.  There are now %i studies in the database." % db.session.query(
                Study).count())
        db.session.commit()

    def load_trainings(self):
        with open(self.training_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                training = Training(id=row[0], title=row[1], description=row[2], outcomes=row[3], image=row[4],
                                    image_caption=row[5])
                db.session.add(training)
            print("Trainings loaded.  There are now %i trainings in the database." % db.session.query(
                Training).count())
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

    def clear(self):
        db.session.query(EmailLog).delete()
        db.session.query(StarResource).delete()
        db.session.query(Study).delete()
        db.session.query(Training).delete()
        db.session.query(User).delete()
        db.session.commit()
