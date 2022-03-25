from unittest import TestCase

from flask import jsonify

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        games = {'b8d2639c-21bd-4aa3-9a92-524ef979c6fe':
        '<BoggleGame board=LKELT.DKSKE.AALNP.PIATE.ARJUA played_words=set()>'}

        self.client = app.test_client()
        app.config['TESTING'] = True




    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            # test that you're getting a template
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<title>Boggle", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            json = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.is_json)
            self.assertIn("gameId" and "board", json)
            self.assertFalse(len(games) == 0)
            # write a test for this route


