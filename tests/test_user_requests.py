from unittest import TestCase
import mock

from skill.user_requests import build_speechlet_response, build_response, get_welcome_response, get_help_response, \
    handle_session_end_request, get_next_meetup


class UserRequestsTestCase(TestCase):
    """ Tests User Request responses.
    """

    def test_build_speechlet_response(self):
        expected = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'hello david'
            },
            'card': {
                'type': 'Simple',
                'title': 'Hello',
                'content': 'hello david'
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': "I can't do that david"
                }
            },
            'shouldEndSession': False
        }
        self.assertEqual(
            build_speechlet_response(
                'Hello',
                'hello david',
                "I can't do that david",
                False
            ),
            expected
        )

    def test_build_response(self):
        expected = {
            'version': '1.0',
            'sessionAttributes': 'attrs',
            'response': 'response'
        }

        self.assertEqual(
            build_response('attrs', 'response'),
            expected
        )

    def test_handle_session_end_request(self):
        expected = build_response(
            {},
            build_speechlet_response(
                'Goodbye',
                'Thank you and have a great day!',
                None,
                True
            )
        )
        self.assertEqual(handle_session_end_request(), expected)

    def test_get_help_response(self):
        expecedt = build_response(
            {},
            build_speechlet_response(
                'Help',
                'Please ask me what time is the next Meetup',
                'Please ask me when is the next Meetup',
                False)
        )
        self.assertEqual(get_help_response(), expecedt)

    def test_get_welcome_response(self):
        expected = build_response(
            {},
            build_speechlet_response(
                'Welcome',
                'Welcome to Boston Python we have Meetups twice a month',
                'Please ask me when is the next Meetup',
                False
            )
        )
        self.assertEqual(get_welcome_response(), expected)

    @mock.patch('skill.user_requests.requests')
    @mock.patch('skill.user_requests.build_response')
    @mock.patch('skill.user_requests.build_speechlet_response')
    def test_get_next_meetup_future(self, build_speechlet_response, build_response, requests):
        build_response.return_value = 'response'
        build_speechlet_response.return_value = 'speechlet'

        result = mock.Mock()
        result.status_code = 200
        result.json.return_value = [
            {
                'local_date': '1992-01-20',
                'local_time': '13:22',
                'name': 'Test Meetup'
            }, {
                'local_date': '3992-01-20',
                'local_time': '18:22',
                'name': 'Test Meetup'
            }]

        requests.get.return_value = result
        response_text = 'The next Meetup is Test Meetup and ' \
                        'is scheduled on January 20 at 6 22 PM'

        self.assertEqual('response', get_next_meetup())
        self.assertResponse(build_speechlet_response, build_response, response_text)

    @mock.patch('skill.user_requests.requests')
    @mock.patch('skill.user_requests.build_response')
    @mock.patch('skill.user_requests.build_speechlet_response')
    def test_get_next_meetup_empty(self, build_speechlet_response, build_response, requests):
        build_response.return_value = 'response'
        build_speechlet_response.return_value = 'speechlet'

        result = mock.Mock()
        result.status_code = 200
        result.json.return_value = []

        requests.get.return_value = result
        response_text = 'I am sorry there does not seem ' \
                        'to be a new meetup scheduled.'

        self.assertEqual('response', get_next_meetup())
        self.assertResponse(build_speechlet_response, build_response, response_text)

    @mock.patch('skill.user_requests.requests')
    @mock.patch('skill.user_requests.build_response')
    @mock.patch('skill.user_requests.build_speechlet_response')
    def test_get_next_meetup_past(self, build_speechlet_response, build_response, requests):
        build_response.return_value = 'response'
        build_speechlet_response.return_value = 'speechlet'

        result = mock.Mock()
        result.status_code = 200
        result.json.return_value = [{
            'local_date': '1992-01-20',
            'local_time': '18:22',
            'name': 'Test Meetup'
        }]

        requests.get.return_value = result
        response_text = 'I am sorry there does ' \
                        'not seem to be a new meetup scheduled.'

        self.assertEqual('response', get_next_meetup())
        self.assertResponse(build_speechlet_response, build_response, response_text)

    def assertResponse(self, build_speechlet_response, build_response, text):
        build_speechlet_response.assert_called_with(
            'Next Meetup',
            text.strip(),
            None,
            True
        )
        build_response.assert_called_with({}, 'speechlet')