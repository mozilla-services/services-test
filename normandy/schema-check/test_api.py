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


def filter_show_heartbeat(record):
    return record['name'] == 'show-heartbeat'


def test_actions(conf, env):
    r = requests.get(conf.get(env, 'api_root') + '/action')
    response = r.json()

    # Verify we have at least one response and then grab the first record
    assert len(response) >= 1
    record = response[0]

    # Does an 'action' have all the required fields?
    expected_action_fields = [
        'name',
        'implementation_url',
        'arguments_schema'
    ]
    for field in record:
        assert field in expected_action_fields

    # Do we have the correct 'arguments_schema' fields?
    expected_arguments_schema_fields = [
        'required',
        'title',
        '$schema',
        'description',
        'type',
        'properties'
    ]
    for field in record['arguments_schema']:
        assert field in expected_arguments_schema_fields

    # Is 'arguments_schema' built correctly?
    assert 'message' in record['arguments_schema']['required']

    # Are properties build correctly
    expected_properties_fields = [
        'description',
        'type',
        'default'
    ]
    for field in record['arguments_schema']['properties']['message']:
        assert field in expected_properties_fields

    # Let's find at least one record that is a 'show-heartbeat'
    sh_records = list(filter(filter_show_heartbeat, response))

    if len(sh_records) > 0:
        show_hearbeat_test(sh_records[0])
    else:
        assert False


def show_hearbeat_test(sh_record):
    expected_action_fields = [
        'name',
        'implementation_url',
        'arguments_schema'
    ]
    for field in sh_record:
        assert field in expected_action_fields

    # Look for our show-heartbeat specific arguments_schema fields
    expected_sh_arguments_schema_fields = [
        'description',
        'title',
        '$schema',
        'required',
        'type',
        'properties',
        'definitions'
    ]
    for field in sh_record['arguments_schema']:
        assert field in expected_sh_arguments_schema_fields

    # Let's check for the properties associated with heartbeats
    expected_sh_properies = [
        'defaults',
        'surveyId',
        'surveys'
    ]

    # Do we have our expected show-hearbeat properties?
    for field in sh_record['arguments_schema']['properties']:
        assert field in expected_sh_properies

    # Check that our properties look as expected
    properties = sh_record['arguments_schema']['properties']

    # Are the default fields there?
    expected_sh_properties_defaults = [
        'description',
        'title',
        'propertyOrder',
        '$ref'
    ]
    for field in properties['defaults']:
        assert field in expected_sh_properties_defaults

    # Are the surveyId fields there as expected?
    expected_sh_properties_surveyId = [
        'description',
        'type',
        'propertyOrder'
    ]
    for field in properties['surveyId']:
        assert field in expected_sh_properties_surveyId

    # Are the survey fields there as expected?
    expected_sh_properties_surveys = [
        'minItems',
        'format',
        'type',
        'items',
        'propertyOrder'
    ]
    for field in properties['surveys']:
        assert field in expected_sh_properties_surveys

    # Look for expected item fields inside the surveys
    expected_survey_items_fields = [
        '$ref',
        'headerTemplate'
    ]
    for field in properties['surveys']['items']:
        assert field in expected_survey_items_fields

    # Do we have the fields we expect in our definitions?
    definitions = sh_record['arguments_schema']['definitions']

    expected_definitions = [
        'message',
        'title',
        'postAnswerUrl',
        'survey',
        'engagementButtonLabel',
        'thanksMessage',
        'learnMoreUrl',
        'learnMoreMessage',
        'weightedSurvey'
    ]
    for field in definitions:
        assert field in expected_definitions

    # Some fields are standardized on description, type, default
    default_fields = [
        'description',
        'type',
        'default'
    ]
    standard_fields = [
        'message',
        'title',
        'postAnswerUrl',
        'engagementButtonLabel',
        'thanksMessage',
        'learnMoreUrl',
        'learnMoreMessage'
    ]
    for field in standard_fields:
        for key in default_fields:
            assert key in definitions[field]

    # Defined surveys have some standard fields as well
    expected_definition_survey_fields = [
        'type',
        'properties'
    ]
    expected_definition_survey_properties_fields = [
        '$ref',
        'propertyOrder'
    ]
    for field in expected_definition_survey_fields:
        assert field in definitions['survey']

    for x in definitions['survey']['properties']:
        for key in definitions['survey']['properties'][x]:
            assert key in expected_definition_survey_properties_fields

    # Check that our 'weightedSurvey' fields all make sense
    weighted_survey = definitions['weightedSurvey']
    property_weight_fields = [
        'minimum',
        'description',
        'type',
        'default',
        'propertyOrder'
    ]
    property_title_fields = [
        '$ref',
        'propertyOrder'
    ]
    assert weighted_survey['allOf']

    # Make sure our various expected fields exist
    for item in weighted_survey['allOf']:
        if '$ref' in item:
            assert True
        elif 'properties' in item:
            for key in item['properties']['weight']:
                assert key in property_weight_fields
            for key in item['properties']['title']:
                assert key in property_title_fields
        elif 'required' in item:
            if 'weight' in item:
                assert True
        else:
            assert False
