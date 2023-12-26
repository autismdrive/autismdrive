import flask_restful
from flask import request
from sqlalchemy import cast, Integer

from app.database import session
from app.models import Category, Study, StudyCategory
from app.models import StudyCategory
from app.rest_exception import RestException
from app.schemas import StudyCategorySchema, CategoryStudiesSchema, StudyCategoriesSchema


class StudyByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryStudiesSchema()

    def get(self, category_id):
        study_categories = (
            session.query(StudyCategory)
            .join(StudyCategory.study)
            .filter(StudyCategory.category_id == cast(category_id, Integer))
            .order_by(Study.title)
            .all()
        )
        return self.schema.dump(study_categories, many=True)


class CategoryByStudyEndpoint(flask_restful.Resource):

    schema = StudyCategoriesSchema()

    def get(self, study_id):
        study_categories = (
            session.query(StudyCategory)
            .join(StudyCategory.category)
            .filter(StudyCategory.study_id == cast(study_id, Integer))
            .order_by(Category.name)
            .all()
        )
        return self.schema.dump(study_categories, many=True)

    def post(self, study_id):
        request_data = request.get_json()

        for item in request_data:
            item["study_id"] = study_id

        study_categories = self.schema.load(request_data, many=True)
        session.query(StudyCategory).filter_by(study_id=cast(study_id, Integer)).delete()
        for c in study_categories:
            session.add(StudyCategory(study_id=study_id, category_id=c.category_id))
        session.commit()
        return self.get(study_id)


class StudyCategoryEndpoint(flask_restful.Resource):
    schema = StudyCategorySchema()

    def get(self, id):
        model = session.query(StudyCategory).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(StudyCategory).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None


class StudyCategoryListEndpoint(flask_restful.Resource):
    schema = StudyCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data)
        session.query(StudyCategory).filter_by(
            study_id=load_result.study_id, category_id=load_result.category_id
        ).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
