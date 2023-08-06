# -*- coding: utf-8 -*-

"""Main module."""
###################################################################################################
#### Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
####
#### Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
#### except in compliance with the License. A copy of the License is located at
####
####     http://aws.amazon.com/apache2.0/
####
#### or in the "license" file accompanying this file. This file is distributed on an "AS IS"
#### BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#### License for the specific language governing permissions and limitations under the License.
###################################################################################################
import boto3
import re
import logging
import time
import yaml
import botocore
import os

RESPONSE_ATTR_DIALOG_STATE = 'dialogState'
RESPONSE_ATTR_SESSION = 'sessionAttributes'
RESPONSE_ATTR_MESSAGE = 'message'
RESPONSE_ATTR_SLOTS = 'slots'
TEST_RESULT_OVERALL_SUCCESS = 'overall_success'

DEFAULT_REGION = 'us-east-1'

logger = logging.getLogger(__name__)


def check(post_conditions, response, attribute, return_value):
    """checks conditions against the response attributes

    :param post_conditions: list of post conditions
    :param response: response received from post_text to Lex
    :param attribute: attribute in post_condition and response to check against
    :param return_value: current test results to update
    :return: result for current test conditions
    """
    att_test_value = post_conditions[attribute] if attribute in post_conditions else []
    if att_test_value:
        att_response_value = response[attribute] if attribute in response else None
        if att_response_value:
            if attribute == 'slots':
                logger.info("att_response_value: {}att_test_value: {}".format(att_response_value, att_test_value))
                return_value[attribute] = True
                for k, v in att_test_value.items():
                    logger.debug("match {} against {}".format(str(v), att_response_value[k]))
                    if not re.match(str(v), att_response_value[k]):
                        logger.error("slots don't match. Should be: {}: {}, but received: {}: {}".format(k, v, k, att_response_value[k]))
                        return_value[attribute] = False
                return return_value
            logger.debug("response: {}: {}".format(attribute, att_response_value))
            for valid_pattern in att_test_value:
                if re.match(valid_pattern, att_response_value):
                    return_value[attribute] = True
                    return return_value
        else:
            logger.error("no response for slots. {}".format(response))
    else:
        # No messages to check, also True
        return_value[attribute] = True
    return return_value


def test_response(response, postConditions):
    """
        go through attributes to test and create complete result
    Args:
        response:
        postConditions:

    :param response: response received from post_text to Lex
    :param postConditions: success conditions from test sequence
    :return: full test results
    """
    return_value = {TEST_RESULT_OVERALL_SUCCESS: False, RESPONSE_ATTR_MESSAGE: False,
                    RESPONSE_ATTR_SESSION: False, RESPONSE_ATTR_SLOTS: False, RESPONSE_ATTR_DIALOG_STATE: False}

    return_value = check(postConditions, response, RESPONSE_ATTR_MESSAGE, return_value)
    return_value = check(postConditions, response, RESPONSE_ATTR_SESSION, return_value)
    return_value = check(postConditions, response, RESPONSE_ATTR_DIALOG_STATE, return_value)
    return_value = check(postConditions, response, RESPONSE_ATTR_SLOTS, return_value)

    return_value[TEST_RESULT_OVERALL_SUCCESS] = return_value[RESPONSE_ATTR_MESSAGE] and return_value[RESPONSE_ATTR_SESSION] and return_value[
        RESPONSE_ATTR_DIALOG_STATE] and return_value[RESPONSE_ATTR_SLOTS]

    return return_value


def setup_boto3_client(region, boto3_client='lex-models'):
    try:
        lex_client = boto3.client(boto3_client) \
            if not region \
            else boto3.client(boto3_client, region_name=region)
    except botocore.exceptions.NoRegionError:
        logger.warning("no region defined or configured, going to default to: {}".format(DEFAULT_REGION))
        lex_client = boto3.client(boto3_client, region_name=DEFAULT_REGION)
    except ValueError as e:
        logger.warning("ValueError: {}. Going to default to default region: {}".format(e, DEFAULT_REGION))
        lex_client = boto3.client(boto3_client, region_name=DEFAULT_REGION)
    return lex_client


def run_test(test_sequence_file_path, lex_alias, region='us-east-1', example=None, log_level='INFO'):
    """ Takes a sequence test file and runs the conversations checking the post condition. Will exit with error when post condition is not met.

    :param test_sequence_file_path: path to test file
    :param lex_alias: alias to test against
    :return: Exception when post conditions are not met
    """

    if example:
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        test_sequence_file_path = os.path.join(SCRIPT_DIR, "examples/{}_Test.yaml".format(example))

    full_test_results = []
    logger.setLevel(log_level)

    with open(test_sequence_file_path) as test_sequences_file:
        test_definition = yaml.load(test_sequences_file)

        botName = test_definition['botName']

        lex_client = setup_boto3_client(region, boto3_client='lex-runtime')

        botAlias = test_definition['botAlias'] if not lex_alias else lex_alias
        logger.info("testing against lex_alias: {}".format(lex_alias))
        userId = re.sub("[^0-9a-zA-Z._:-]", "-", botName + '-' + botAlias + '-' + str(time.time()))

        logger.debug(test_definition)
        for sequence in test_definition['sequences']:
            sequence_name = sequence['name']
            logger.info("============== sequence: %s =============   start   ===========", sequence_name)
            sessionAttributes = {}
            requestAttributes = {}
            step_number = 0
            for step in sequence['sequence']:
                step_number += 1
                logger.info("================= step: %s ======== start ==============", step_number)
                logger.debug("step : %s", step)
                input_text = step['utterance']
                logger.info("utterance: %s", input_text)

                response = lex_client.post_text(botName=botName,
                                                botAlias=botAlias,
                                                userId=userId,
                                                sessionAttributes=sessionAttributes,
                                                requestAttributes=requestAttributes,
                                                inputText=input_text)
                logger.debug(response)

                test_result = test_response(response, step['postConditions'])
                logger.info("test_result: {}".format(test_result))
                if not test_result[TEST_RESULT_OVERALL_SUCCESS]:
                    test_fail_message = "test failed (success = {} ) for {} at {}-{}".format(test_result[TEST_RESULT_OVERALL_SUCCESS], input_text, sequence_name, step_number)
                    logger.error(test_fail_message)
                else:
                    logger.info("rest-result: {} == {}-{}".format(test_result[TEST_RESULT_OVERALL_SUCCESS], sequence_name, step_number))
                # hand over session attributes for next call
                full_test_results.append({"name": sequence_name, "step_number": step_number, "input_text": input_text, "result": test_result})
                sessionAttributes = response['sessionAttributes']
                logger.info("================= step: %s ======== finished ==============", step_number)
            logger.info("============== sequence: %s =============   stop   ===========", sequence_name)
    all_tests_succeed = False
    for i, r in enumerate(full_test_results):
        logger.info(r) if r['result'][TEST_RESULT_OVERALL_SUCCESS] else logger.error(r)

        all_tests_succeed = all_tests_succeed or r['result'][TEST_RESULT_OVERALL_SUCCESS]

    if not all_tests_succeed:
        raise Exception('not all tests succeeded. results: {} '.format(full_test_results))
