import unittest

from flask import json

from tests.base_test import BaseTest
from app import db
from app.model.chain_step import ChainStep
from app.model.questionnaires.chain_session_step import ChainSessionStep


class TestChainStep(BaseTest, unittest.TestCase):

    def test_chain_step_basics(self):
        self.construct_chain_step()
        chain_step = db.session.query(ChainStep).first()
        self.assertIsNotNone(chain_step)
        rv = self.app.get('/api/chain_step/%i' % chain_step.id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], chain_step.id)

    def test_modify_chain_step_basics(self):
        self.construct_chain_step()
        chain_step = db.session.query(ChainStep).first()
        self.assertIsNotNone(chain_step)
        rv = self.app.get('/api/chain_step/%i' % chain_step.id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['instruction'] = 'Take out the trash'
        rv = self.app.put('/api/chain_step/%i' % chain_step.id, data=self.jsonify(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        db.session.commit()
        rv = self.app.get('/api/chain_step/%i' % chain_step.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['instruction'], 'Take out the trash')

    def test_delete_chain_step(self):
        chain_step = self.construct_chain_step()
        chain_step_id = chain_step.id
        rv = self.app.get('api/chain_step/%i' % chain_step_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/chain_step/%i' % chain_step_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/chain_step/%i' % chain_step_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_disallow_deleting_chain_step_if_being_used(self):
        chain_step = self.construct_chain_step()
        chain_step_id = chain_step.id

        db.session.add(ChainSessionStep(chain_step_id=chain_step_id))
        db.session.commit()

        rv = self.app.get('api/chain_step/%i' % chain_step_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/chain_step/%i' % chain_step_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.json['code'], 'can_not_delete')

    def test_multiple_chain_steps(self):
        chain_steps = self.construct_chain_steps()
        self.assertEqual(4, len(chain_steps))
        rv = self.app.get('/api/chain_step', follow_redirects=True, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(chain_steps), len(response))

