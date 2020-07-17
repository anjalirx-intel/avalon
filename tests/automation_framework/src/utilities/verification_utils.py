import json
import logging
import avalon_crypto_utils.signature as signature
import avalon_crypto_utils.crypto_utility as enclave_helper
import env
from error_code.error_status import SignatureStatus
from error_code.error_status import WorkOrderStatus
from src.utilities.worker_utilities import ResultStatus
import base64

logger = logging.getLogger(__name__)


def validate_response_code(response, expected_res):
    """ Function to validate work order response.
        Input Parameters : response, check_result
        Returns : err_cd"""
    # check expected key of test case
    check_result = {"error": {"code": 5}}
    check_result_key = list(check_result.keys())[0]
    # check response code
    if check_result_key in response:
        if "code" in check_result[check_result_key].keys():
            if "code" in response[check_result_key].keys():
                if (response[check_result_key]["code"] ==
                        expected_res):
                    err_cd = 0
                    if expected_res == 0:
                        logger.info('SUCCESS: Worker API response "%s"!!',
                                    response[check_result_key]["message"])
                    elif expected_res == 2:
                        logger.info(
                            'Invalid parameter format in response "%s".',
                            response[check_result_key]["message"])
                    elif expected_res == 5:
                        logger.info('SUCCESS: WorkOrderSubmit response'
                                    ' key error and status (%s)!!\
                                 \n', check_result[check_result_key]["code"])
                else:
                    err_cd = 1
                    logger.info(
                        'ERROR: Response did not contain expected code '
                        '%s.\n', check_result[check_result_key]["code"])
            else:
                err_cd = 1
                logger.info('ERROR: Response did not contain expected \
                         code %s. \n', check_result[check_result_key]["code"])
    else:
        check_get_result = '''{"result": {"workOrderId": "", "workloadId": "",
                        "workerId": "", "requesterId": "", "workerNonce": "",
                               "workerSignature": "", "outData": ""}}'''

        check_result = json.loads(check_get_result)

        check_result_key = list(check_result.keys())[0]

        if check_result_key == "result":
            if (set(check_result["result"].keys()).issubset
               (response["result"].keys())):

                # Expected Keys : check_result["result"].keys()
                # Actual Keys : response["result"].keys()
                err_cd = 0
                logger.info('SUCCESS: WorkOrderGetResult '
                            'response has keys as expected!!')
            else:
                err_cd = 1
                logger.info('ERROR: Response did not contain keys \
                as expected in for test case. ')
        else:
            err_cd = 0
            logger.info('No validation performed for the expected result \
            in validate response. ')

    return err_cd


def is_valid_params(request_elements, keys_count=None):
    """
    Fucntion to check the number of parameters in submit requests.
    """
    if keys_count:
        request_keys = sum(keys_count(elem) for elem in request_elements)
    return request_keys


def verify_work_order_signature(response, worker_obj, requester_nonce):
    verify_key = worker_obj['result']['details']['workerTypeData']['verificationKey']

    try:
        verify_obj = signature.ClientSignature()
        sig_bool = verify_obj.verify_signature(response, verify_key, requester_nonce)

        if sig_bool is SignatureStatus.PASSED:
            err_cd = 0
            logger.info('Success: Work Order Signature Verified.')
        else:
            err_cd = 1
            logger.info('ERROR: Work Order Signature Verification Failed')
    except Exception:
        err_cd = 1
        logger.error('ERROR: Failed to analyze Signature Verification')

    return err_cd


def decrypt_work_order_response(response, session_key, session_iv):
    decrypted_data = ""
    try:
        decrypted_data = enclave_helper.decrypted_response(response,
                                                           session_key,
                                                           session_iv)
        err_cd = 0
        logger.info('Success: Work Order Response Decrypted.\n\n')
    except Exception as e:
        err_cd = 1
        logger.exception('Exception: Decryption failed %s \
                           where expected. \n', e)
        logger.error('ERROR: Work Order Response Decryption Failed')

    return err_cd, decrypted_data

def decode_work_order_response(out_data):
    decode_data_err = 1
    output = []
    try:
        for result in out_data:
            data = result["data"]
            output.append(base64.b64decode(data).decode('UTF-8'))
        decode_data_err = 0
        logger.info("Data is %s.\n", output)
    except Exception as e:
        logger.exception("Error occured during decoding of data, %s.\n", e)
    return decode_data_err, output


def verify_test(response, expected_res, worker_obj, work_order_obj):
    if type(work_order_obj) != dict:
        session_key = work_order_obj.session_key
        session_iv = work_order_obj.session_iv
        requester_nonce = work_order_obj.params_obj["requesterNonce"]
    else:
        session_key = work_order_obj["sessionKey"]
        session_iv = work_order_obj["sessionKeyIv"]
        requester_nonce = work_order_obj["requesterNonce"]

    outData = response.get("result", {}).get("outData", [])
    if len(outData) > 1:
        decode_result = all([x.get("encryptedDataEncryptionKey") == "-" for x in outData])
    else:
        decode_result = False
    if decode_result:
        decode_wo_response_err = decode_work_order_response(outData)[0]

        assert (decode_wo_response_err is ResultStatus.SUCCESS.value)
    else:
        verify_wo_signature_err = verify_work_order_signature(response['result'],
                                                          worker_obj, requester_nonce)

        assert (verify_wo_signature_err is ResultStatus.SUCCESS.value)

        decrypt_wo_response_err = decrypt_work_order_response(response['result'],
                                                          session_key,
                                                          session_iv)[0]

        assert (decrypt_wo_response_err is ResultStatus.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    validate_response_code_err = validate_response_code(
        response, expected_res)

    assert (validate_response_code_err is ResultStatus.SUCCESS.value)

    return ResultStatus.SUCCESS.value

def check_worker_lookup_response(response, operator, value):
    if env.proxy_mode:
        if operator(response[0], value):
            err_cd = 0
        else:
            err_cd = 1
    else:
        if operator(response["result"]["totalCount"], value):
            err_cd = 0
        else:
            err_cd = 1
    return err_cd


def check_worker_retrieve_response(response):
    if response["result"]["workerType"] == 1:
        err_cd = 0
    else:
        err_cd = 1

    return err_cd


def check_worker_create_receipt_response(response):

    if env.blockchain_type == "ethereum":
        if response[0] == 1:
            err_cd = 0
        else:
            err_cd = 1
    else:
        if response["error"]["code"] == 0:
            err_cd = 0
        else:
            err_cd = 1

    return err_cd


def check_worker_retrieve_receipt_response(response):
    if env.blockchain_type == "ethereum":
        if response[0] == 1:
            err_cd = 0
        else:
            err_cd = 1
    else:
        if response["result"]["updateType"] == 2:
            err_cd = 0
        else:
            err_cd = 1

    return err_cd


def check_negative_test_responses(response, expected_res):
    error_msg = response.get("error", {}).get("message")
    if expected_res == "Invalid data format for work order id":
        if error_msg == "Invalid data format for work order id" or\
            (error_msg == "Server error" and
                response["error"]["data"]["message"] == "'workOrderId'"):
            return ResultStatus.SUCCESS.value

    if expected_res == error_msg:
        return ResultStatus.SUCCESS.value

    if (response.get("error", {}).get("code") == -1) and env.proxy_mode:
        return ResultStatus.SUCCESS.value


def check_workorder_receipt_lookup_response(response, operator, value):

    ''' if env.blockchain_type == "ethereum":
        if operator(response[0], value):
            err_cd = 0
        else:
            err_cd = 1
    else:'''
    if env.blockchain_type == "fabric":
        if operator(response[0], value):
            err_cd = 0
        else:
            err_cd = 1
    else:
        if operator(response["result"]["totalCount"], value):
            err_cd = 0
        else:
            err_cd = 1
    return err_cd
