import flask_restful
from flask import request

from app import db, RestException
from app.model.category import Category
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.schema.schema import StudyCategorySchema, CategoryStudiesSchema, StudyCategoriesSchema


class StudyByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryStudiesSchema()

    def get(self, category_id):
        study_categories = db.session.query(StudyCategory)\
            .join(StudyCategory.study)\
            .filter(StudyCategory.category_id == category_id)\
            .order_by(Study.title)\
            .all()
        return self.schema.dump(study_categories, many=True)


class CategoryByStudyEndpoint(flask_restful.Resource):

    schema = StudyCategoriesSchema()

    def get(self, study_id):
        study_categories = db.session.query(StudyCategory).\
            join(StudyCategory.category).\
            filter(StudyCategory.study_id == study_id).\
            order_by(Category.name).\
            all()
        return self.schema.dump(study_categories,many=True)

    def post(self, study_id):
        request_data = request.get_json()

        for item in request_data:
            item['study_id'] = study_id

        study_categories = self.schema.load(request_data, many=True)
        db.session.query(StudyCategory).filter_by(study_id=study_id).delete()
        for c in study_categories:
            db.session.add(StudyCategory(study_id=study_id,
                           category_id=c.category_id))
        db.session.commit()
        return self.get(study_id)


class StudyCategoryEndpoint(flask_restful.Resource):
    schema = StudyCategorySchema()

    def get(self, id):
        model = db.session.query(StudyCategory).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(StudyCategory).filter_by(id=id).delete()
        db.session.commit()
        return None


class StudyCategoryListEndpoint(flask_restful.Resource):
    schema = StudyCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data)
        db.session.query(StudyCategory).filter_by(study_id=load_result.study_id,
                                                  category_id=load_result.category_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
