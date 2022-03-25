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
            json = response.json

            self.assertEqual(response.status_code, 200)
            self.assertTrue(json['gameId'])
            self.assertTrue(type(json['board']) is list)
            self.assertTrue(type(json['board'][0])is list)
            self.assertIn(json['gameId', games])
            # write a test for this route

    def test_api_score_word(self):
        """Testing the score-word endpoint"""

        with self.client as client:
            new_game_response = client.post("/api/new-game")
            json_response = new_game_response.get_json()
            response_id = json_response['gameId']
            game = games[response_id]

            game.board[0] = ['A', 'P', 'P', 'L', 'E']
            game.board[1] = ['Z', 'Z', 'Z', 'Z', 'Z']
            game.board[2] = ['Z', 'Z', 'Z', 'Z', 'Z']
            game.board[3] = ['Z', 'Z', 'Z', 'Z', 'Z']
            game.board[4] = ['Z', 'Z', 'Z', 'Z', 'Z']

            check_word_response = client.post("/api/score-word",
            json={"gameId" : response_id, "word" : 'APPLE'})
            check_word_response_json = check_word_response.get_json()
            self.assertEqual(check_word_response_json, {'result': 'ok'})

            check_word_response = client.post("/api/score-word",
            json={"gameId" : response_id, "word" : 'TACO'})
            check_word_response_json = check_word_response.get_json()
            self.assertEqual(check_word_response_json, {'result': 'not-on-board'})

            check_word_response = client.post("/api/score-word",
            json={"gameId" : response_id, "word" : 'FDSH'})
            check_word_response_json = check_word_response.get_json()
            self.assertEqual(check_word_response_json, {'result': 'not-word'})



