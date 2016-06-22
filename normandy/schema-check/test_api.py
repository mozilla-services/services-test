import configparser
import pytest
import requests


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_recipies(conf, env):
    r = requests.get(conf.get(env, 'api_root') + '/recipe')
    response = r.json()
    expected_fields = [
        'id',
        'last_updated',
        'name',
        'enabled',
        'revision_id',
        'action',
        'arguments',
        'filter_expression',
        'current_approval_request',
        'approval',
        'is_approved'
    ]

    expected_arguments = [
        'defaults',
        'surveyId',
        'surveys'
    ]

    expected_survey_fields = [
        'message',
        'thanksMessage',
        'engagementButtonLabel',
        'title',
        'postAnswerUrl',
        'weight',
        'learnMoreUrl',
        'learnMoreMessage',
    ]

    expected_default_fields = [
        'message',
        'thanksMessage',
        'engagementButtonLabel',
        'postAnswerUrl',
        'learnMoreUrl',
        'learnMoreMessage'
    ]

    # Verify we have at least one response
    assert len(response) >= 1

    # Take a look at the first response and look for the expected fields
    record = response[0]
    for field in expected_fields:
        assert field in record

    # Do the arguments look right?
    for argument in expected_arguments:
        assert argument in record['arguments']

    # Do the defaults look right?
    for field in record['arguments']['defaults']:
        assert field in expected_default_fields

    # Do survey fields look right? Look at the first one
    for field in record['arguments']['surveys'][0]:
        assert field in expected_survey_fields
