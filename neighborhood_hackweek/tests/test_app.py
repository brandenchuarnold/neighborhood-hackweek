from neighborhood_hackweek.main import app
from nose.tools import eq_, ok_


class TestApp(object):

    def setup(self):
        self.actual_app = app
        self.app = self.actual_app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        eq_(resp.status_code, 200)
        ok_("Hello World" in resp.data)
