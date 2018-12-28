import flask_restful
from flask import request

from app import db, RestException
from app.model.category import Category
from app.model.training import Training
from app.model.training_category import TrainingCategory
from app.resources.schema import TrainingCategorySchema, CategoryTrainingsSchema, TrainingCategoriesSchema


class TrainingByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryTrainingsSchema()

    def get(self, category_id):
        training_categories = db.session.query(TrainingCategory)\
            .join(TrainingCategory.training)\
            .filter(TrainingCategory.category_id == category_id)\
            .order_by(Training.title)\
            .all()
        return self.schema.dump(training_categories, many=True)


class CategoryByTrainingEndpoint(flask_restful.Resource):

    schema = TrainingCategoriesSchema()

    def get(self, training_id):
        training_categories = db.session.query(TrainingCategory).\
            join(TrainingCategory.category).\
            filter(TrainingCategory.training_id == training_id).\
            order_by(Category.name).\
            all()
        return self.schema.dump(training_categories,many=True)

    def post(self, training_id):
        request_data = request.get_json()
        training_categories = self.schema.load(request_data, many=True).data
        db.session.query(TrainingCategory).filter_by(training_id=training_id).delete()
        for c in training_categories:
            db.session.add(TrainingCategory(training_id=training_id,
                           category_id=c.category_id))
        db.session.commit()
        return self.get(training_id)


class TrainingCategoryEndpoint(flask_restful.Resource):
    schema = TrainingCategorySchema()

    def get(self, id):
        model = db.session.query(TrainingCategory).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(TrainingCategory).filter_by(id=id).delete()
        db.session.commit()
        return None


class TrainingCategoryListEndpoint(flask_restful.Resource):
    schema = TrainingCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(TrainingCategory).filter_by(training_id=load_result.training_id,
                                                     category_id=load_result.category_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
