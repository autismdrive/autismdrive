import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError

from app import RestException, db
from app.model.training import Training
from app.resources.schema import TrainingSchema


class TrainingEndpoint(flask_restful.Resource):

    schema = TrainingSchema()

    def get(self, id):
        model = db.session.query(Training).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(Training).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Training).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class TrainingListEndpoint(flask_restful.Resource):

    trainingsSchema = TrainingSchema(many=True)
    trainingSchema = TrainingSchema()

    def get(self):
        trainings = db.session.query(Training).all()
        return self.trainingsSchema.dump(trainings)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.trainingSchema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            return self.trainingSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
