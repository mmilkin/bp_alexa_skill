"""
Lambda function orchestrator
"""
from __future__ import print_function

from skill.ids import SKILL_ID

from skill.user_requests import (
    get_help_response,
    get_next_meetup,
    get_welcome_response,
    handle_session_end_request
)



def on_session_started(session_started_request, session):
    """
    Prints sessions start.

    :param session_started_request:
    :param session:
    :return:
    """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == 'NextMeetup':
        return get_next_meetup()
    elif intent_name == 'AMAZON.HelpIntent':
        return get_help_response()
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print('on_session_ended requestId=' + session_ended_request['requestId'] +
          ', sessionId=' + session['sessionId'])


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    print(
        'event.session.application.applicationId='
        + event['session']['application']['applicationId']
    )

    if event['session']['application']['applicationId'] != SKILL_ID:
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == 'SessionEndedRequest':
        return on_session_ended(event['request'], event['session'])
