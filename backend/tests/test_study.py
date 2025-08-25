import random
import smtplib
from unittest.mock import MagicMock, patch

from tests.base_test import BaseTest  # isort:skip
from fixtures.study import MockStudy, MockStudyWithMoreFields
from sqlalchemy import Integer, cast

from app.enums import ParticipantRelationship, Relationship
from app.models import (
    ContactQuestionnaire,
    EmailLog,
    IdentificationQuestionnaire,
    Study,
    StudyCategory,
    StudyInvestigator,
)
from tests.fixtures.fixture_utils import fake


class TestStudy(BaseTest):
    def test_study_basics(self):
        mock_study = MockStudy()
        self.construct_study(**mock_study.__dict__)
        s = self.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.client.get("/api/study/%i" % s_id, follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], s_id)
        self.assertEqual(response["title"], mock_study.title)
        self.assertEqual(response["description"], mock_study.description)
        self.assertNotIn("study_users", response, "Never include info about other users in a non-protected endpoint")
        self.assertNotIn("users", response, "Never include info about other users in a non-protected endpoint")

    def test_modify_study_basics(self):
        self.construct_study()
        s = self.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.client.get("/api/study/%i" % s_id, content_type="application/json")
        modified_study = rv.json.copy()
        orig_date = modified_study["last_updated"]
        mock_study = MockStudyWithMoreFields()
        modified_study.update(mock_study.__dict__)

        rv = self.client.put(
            "/api/study/%i" % s_id,
            data=self.jsonify(modified_study),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        rv = self.client.get("/api/study/%i" % s_id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], mock_study.title)
        self.assertEqual(response["description"], mock_study.description)
        self.assertEqual(response["benefit_description"], mock_study.benefit_description)
        self.assertEqual(response["short_title"], mock_study.short_title)
        self.assertEqual(response["short_description"], mock_study.short_description)
        self.assertEqual(response["image_url"], mock_study.image_url)
        self.assertEqual(response["coordinator_email"], mock_study.coordinator_email)
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_study(self):
        s = self.construct_study()
        s_id = s.id
        admin_headers = self.default_logged_in_headers
        rv = self.client.get("api/study/%i" % s_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.client.delete("api/study/%i" % s_id, content_type="application/json", headers=admin_headers)
        self.assert_success(rv)

        rv = self.client.get("api/study/%i" % s_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_study(self):
        study = MockStudy()
        rv = self.client.post(
            "api/study",
            data=self.jsonify(study),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], study.title)
        self.assertEqual(response["benefit_description"], study.benefit_description)
        self.assertIsNotNone(response["id"])

    def test_get_study_by_category(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study_id=s.id, category_id=c.id)
        self.session.add(cs)
        self.session.commit()
        rv = self.client.get(
            "/api/category/%i/study" % c.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(s.description, response[0]["study"]["description"])

    def test_get_study_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        s = self.construct_study()
        cs = StudyCategory(study_id=s.id, category_id=c.id)
        cs2 = StudyCategory(study_id=s.id, category_id=c2.id)
        self.session.add_all([cs, cs2])
        self.session.commit()
        rv = self.client.get(
            "/api/category/%i/study" % c.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(2, len(response[0]["study"]["study_categories"]))
        self.assertEqual("c1", response[0]["study"]["study_categories"][0]["category"]["name"])

    def test_category_study_count(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study_id=s.id, category_id=c.id)
        self.session.add(cs)
        self.session.commit()
        rv = self.client.get("/api/category/%i" % c.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["study_count"])

    def test_get_category_by_study(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study_id=s.id, category_id=c.id)
        self.session.add(cs)
        self.session.commit()
        rv = self.client.get("/api/study/%i/category" % s.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_study(self):
        c = self.construct_category()
        s = self.construct_study()

        sc_data = {"study_id": s.id, "category_id": c.id}

        rv = self.client.post("/api/study_category", data=self.jsonify(sc_data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_categories_on_study(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        s = self.construct_study()

        sc_data = [
            {"category_id": c1.id},
            {"category_id": c2.id},
            {"category_id": c3.id},
        ]
        rv = self.client.post(
            "/api/study/%i/category" % s.id, data=self.jsonify(sc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        sc_data = [{"category_id": c1.id}]
        rv = self.client.post(
            "/api/study/%i/category" % s.id, data=self.jsonify(sc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))

    def test_remove_category_from_study(self):
        self.test_add_category_to_study()
        rv = self.client.delete("/api/study_category/%i" % 1)
        self.assert_success(rv)
        rv = self.client.get("/api/study/%i/category" % 1, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_add_investigator_to_study(self):
        i = self.construct_investigator()
        s = self.construct_study()

        si_data = {"study_id": s.id, "investigator_id": i.id}

        rv = self.client.post(
            "/api/study_investigator",
            data=self.jsonify(si_data),
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(i.id, response["investigator_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_investigators_on_study(self):
        headers = self.default_logged_in_headers
        i1 = self.construct_investigator(name="person1")
        i2 = self.construct_investigator(name="person2")
        i3 = self.construct_investigator(name="person3")
        s = self.construct_study()

        si_data = [
            {"investigator_id": i1.id},
            {"investigator_id": i2.id},
            {"investigator_id": i3.id},
        ]
        rv = self.client.post(
            "/api/study/%i/investigator" % s.id,
            data=self.jsonify(si_data),
            content_type="application/json",
            headers=headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        si_data = [{"investigator_id": i1.id}]
        rv = self.client.post(
            "/api/study/%i/investigator" % s.id,
            data=self.jsonify(si_data),
            content_type="application/json",
            headers=headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))

    def test_remove_investigator_from_study(self):
        self.test_add_investigator_to_study()
        rv = self.client.delete("/api/study_investigator/%i" % 1, headers=self.default_logged_in_headers)
        self.assert_success(rv)
        rv = self.client.get("/api/study/%i/investigator" % 1, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    @patch("smtplib.SMTP", autospec=True)
    def test_study_inquiry_sends_email(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        s = self.construct_study(title=fake.catch_phrase())
        u = self.default_user
        u_headers = self.logged_in_headers(user_id=u.id)
        guardian = self.construct_participant(user_id=u.id, relationship=Relationship.self_guardian)
        dependent1 = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
        self.construct_contact_questionnaire(user=u, participant=guardian, phone=fake.phone_number(), email=u.email)
        self.construct_identification_questionnaire(
            user=u,
            participant=guardian,
            first_name=fake.first_name(),
            relationship_to_participant=random.choice([r.value for r in ParticipantRelationship]),
        )
        self.construct_identification_questionnaire(
            user=u,
            participant=dependent1,
            first_name=fake.first_name(),
            is_first_name_preferred=False,
            nickname=fake.company(),
        )

        data = {"user_id": u.id, "study_id": s.id}
        rv = self.client.post(
            "/api/study_inquiry",
            data=self.jsonify(data),
            follow_redirects=True,
            content_type="application/json",
            headers=u_headers,
        )
        self.assert_success(rv)
        self.assert_email_sent(mock_sendmail, s.coordinator_email, "Autism DRIVE: Study Inquiry Email")

        logs = self.session.query(EmailLog).all()
        self.assertIsNotNone(logs[-1].tracking_code)

    @patch("smtplib.SMTP", autospec=True)
    def test_study_inquiry_creates_study_user(self, mock_smtp: MagicMock):
        s = self.construct_study(title="The Best Study")
        u = self.default_user

        self.assertEqual(0, len(s.study_users))

        guardian = self.construct_participant(user_id=u.id, relationship=Relationship.self_guardian)
        self.construct_contact_questionnaire(user=u, participant=guardian, phone="540-669-8855")
        self.construct_identification_questionnaire(user=u, participant=guardian, first_name=fake.first_name())

        data = {"user_id": u.id, "study_id": s.id}
        rv = self.client.post(
            "/api/study_inquiry",
            data=self.jsonify(data),
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)

        db_study = self.session.query(Study).filter(Study.id == cast(s.id, Integer)).first()
        self.assertEqual(1, len(db_study.study_users))
        su = db_study.study_users[0]
        self.assertEqual(u.id, su.user_id)
        self.assertEqual(s.id, su.study_id)

    def test_study_inquiry_fails_without_valid_study_or_user(self):
        s = self.construct_study(title="The Best Study")
        u = self.default_user
        guardian = self.construct_participant(user_id=u.id, relationship=Relationship.self_guardian)
        self.construct_contact_questionnaire(user=u, participant=guardian, phone="540-669-8855")
        self.construct_identification_questionnaire(user=u, participant=guardian, first_name=fake.first_name())

        data = {"user_id": u.id, "study_id": 456}
        rv = self.client.post(
            "/api/study_inquiry",
            data=self.jsonify(data),
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assertEqual(400, rv.status_code)
        response = rv.json
        self.assertEqual(response["message"], "Error in finding correct user and study to complete study inquiry")
        data = {"user_id": 456, "study_id": s.id}
        rv = self.client.post(
            "/api/study_inquiry",
            data=self.jsonify(data),
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assertEqual(400, rv.status_code)
        response = rv.json
        self.assertEqual(response["message"], "Error in finding correct user and study to complete study inquiry")

    def construct_identification_questionnaire(
        self,
        relationship_to_participant=None,
        first_name=None,
        is_first_name_preferred=True,
        nickname=None,
        participant=None,
        user=None,
    ):
        user = self.construct_user(email=fake.email()) if user is None else user
        participant = (
            self.construct_participant(user_id=user.id, relationship=Relationship.dependent)
            if participant is None
            else participant
        )

        iq = IdentificationQuestionnaire(
            relationship_to_participant=relationship_to_participant
            if participant.relationship == Relationship.dependent
            else None,
            relationship_to_participant_other=fake.job()
            if relationship_to_participant == ParticipantRelationship.other
            else None,
            first_name=first_name or fake.first_name(),
            is_first_name_preferred=is_first_name_preferred,
            nickname=nickname or fake.company(),
            participant_id=participant.id,
            user_id=user.id,
        )
        self.session.add(iq)
        self.session.commit()

        db_iq = (
            self.session.query(IdentificationQuestionnaire)
            .filter_by(participant_id=cast(iq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_iq.nickname, iq.nickname)
        return db_iq

    def construct_contact_questionnaire(
        self,
        phone="123-456-7890",
        can_leave_voicemail=True,
        contact_times="whenever",
        email="contact@questionnaire.com",
        participant=None,
        user=None,
    ):
        cq = ContactQuestionnaire(
            phone=phone, can_leave_voicemail=can_leave_voicemail, contact_times=contact_times, email=email
        )
        if user is None:
            u = self.construct_user(email="contact@questionnaire.com")
            cq.user_id = u.id
        else:
            u = user
            cq.user_id = u.id

        if participant is None:
            cq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            cq.participant_id = participant.id

        self.session.add(cq)
        self.session.commit()

        db_cq = self.session.query(ContactQuestionnaire).filter_by(zip=cq.zip).first()
        self.assertEqual(db_cq.phone, cq.phone)
        return db_cq

    def test_delete_study_deletes_relationship(self):
        i = self.construct_investigator()
        i_id = i.id
        s = self.construct_study()
        s_id = s.id
        si = StudyInvestigator(investigator_id=i_id, study_id=s_id)
        self.session.add(si)
        self.session.commit()
        si_id = si.id

        rv = self.client.get(f"/api/study_investigator/{si_id}", content_type="application/json")
        self.assert_success(rv)
        r_dict = rv.json
        self.assertEqual(r_dict["investigator_id"], i_id)
        self.assertEqual(r_dict["study_id"], s_id)

        rv = self.client.delete(
            f"/api/study/{s_id}", content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)

        rv = self.client.get(f"/api/study_investigator/{si_id}", content_type="application/json")
        self.assertEqual(404, rv.status_code)
