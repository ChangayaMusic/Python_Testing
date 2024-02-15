import unittest
from server import app

class UknownEmailTest(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    def test_invalid_email_flash_message(self):
        # Simulate a POST request with an invalid email
        response = self.app.post('/showSummary', data={'email': 'invalid@example.com'})

        # Check if the response redirects to the index page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/'))

        # Follow the redirect to the index page
        response = self.app.get(response.location)

        # Check if the flash message is present
        self.assertIn(b'Invalid email, please try again.', response.data)

if __name__ == '__main__':
    unittest.main()
