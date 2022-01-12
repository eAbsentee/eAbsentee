import unittest
from unittest.mock import patch

from eAbsentee.app import create_app
app = create_app()

class HomeTemplatesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_form_closed(self):
        with patch.dict(self.app.application.config, FORM_OPEN=False):
            index_html = self.app.get('/')
            assert b"The deadline to request an absentee ballot has passed." in index_html.data

    def test_form_open(self):
        with patch.dict(self.app.application.config, FORM_OPEN=True):
            index_html = self.app.get('/')
            # assert links to form are on page

if __name__ == '__main__':
    unittest.main()
