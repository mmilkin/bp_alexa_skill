"""
User Functions.
"""
from datetime import datetime

import requests
import pytz

BOSTON_PYTHON_URL = "https://api.meetup.com/bostonpython?&sign=true&photo-host=public"
BOSTON_PYTHON_EVENTS = "https://api.meetup.com/bostonpython/events"


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Builds speachlet for response.

    :param title:
    :param output:
    :param reprompt_text:
    :param should_end_session:
    :return:
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Build response

    :param session_attributes:
    :param speechlet_response:
    :return:
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def get_next_meetup():
    """
    Finds next meetup.

    :return: response
    """
    result = requests.get(BOSTON_PYTHON_EVENTS)
    assert result.status_code == 200
    json = result.json()
    est = pytz.timezone('EST')
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    for event in json:
        event_date = event['local_date']
        event_time = event['local_time']
        event_datetime = datetime.strptime(
            '{} {}'.format(event_date, event_time),
            '%Y-%m-%d %H:%M'
        )
        event_datetime = est.localize(event_datetime)
        if now < event_datetime:
            break
    else:
        event = None

    if not event or now > event_datetime:
        return build_response({}, build_speechlet_response(
            'Next Meetup', 'I am sorry there does not seem to be a new meetup scheduled.',
            None,
            True
        ))

    name = event.get('name')
    date = event_datetime.strftime('%B %-d')
    minutes = event_datetime.strftime('%M')
    hour = event_datetime.strftime('%-I')
    tod = event_datetime.strftime('%p')

    response_format = 'The next Meetup is {name} and is scheduled ' \
                      'on {date} at {hour} {minutes} {tod}'

    response = response_format.format(
        name=name,
        date=date,
        hour=hour,
        tod=tod,
        minutes=minutes if int(minutes) else '')

    return build_response({}, build_speechlet_response(
        'Next Meetup', response, None, True))


def get_welcome_response():
    """
    Finds welcome response.

    :return:
    """
    response = 'Welcome to Boston Python we have Meetups twice a month'
    reprompt_text = 'Please ask me when is the next Meetup'
    return build_response({}, build_speechlet_response(
        "Welcome", response, reprompt_text, False))


def get_help_response():
    """
    Help response.

    :return:
    """
    response = 'Please ask me what time is the next Meetup'
    reprompt_text = 'Please ask me when is the next Meetup'
    return build_response({}, build_speechlet_response(
        'Help', response, reprompt_text, False))


def handle_session_end_request():
    """
    End session.

    :return:
    """
    card_title = 'Goodbye'
    speech_output = 'Thank you and have a great day!'
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, True))
