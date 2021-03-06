# Copyright 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import logging
import os
import env
from src.libs.avalon_test_wrapper \
    import read_json, submit_request
from src.utilities.worker_utilities import ResultStatus
from src.utilities.verification_utils \
    import verify_test, check_worker_create_receipt_response, \
    check_worker_retrieve_receipt_response, check_workorder_receipt_lookup_response
import operator
from src.libs.test_base import AvalonBase

logger = logging.getLogger(__name__)


class TestClass():
    test_obj = AvalonBase()

    @pytest.mark.work_order_create_receipt
    @pytest.mark.sdk
    @pytest.mark.p1
    @pytest.mark.listener
    def test_work_order_create_receipt_success(self):
        test_id = '18558'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_create_receipt_response(receipt_response)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_retrieve_receipt
    @pytest.mark.sdk
    @pytest.mark.p1
    def test_work_order_retrieve_receipt_success(self):
        test_id = '21233'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt_retrieve.json")

        err_cd = self.test_obj.setup_and_build_request_receipt_retrieve(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_retrieve_receipt_response(receipt_response)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.sdk
    @pytest.mark.listener
    def test_create_work_order_receipt_invalid_requester_id(self):
        test_id = '21234'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt_invalid_requester_id.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_create_receipt_response(receipt_response)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.sdk
    @pytest.mark.listener
    def test_create_work_order_receipt_hexstr_workorderRequesthash(
            self):
        test_id ='21235'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt_hexstr_workorderRequesthash.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_create_receipt_response(receipt_response)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.sdk
    @pytest.mark.listener
    def test_create_work_order_receipt_wrong_rverificationkey(self):
        test_id = '21236'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt_wrong_rverificationkey.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_create_receipt_response(receipt_response)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_receipt_lookup
    @pytest.mark.sdk
    def test_work_order_receipt_lookup_success(self):
        test_id = '18605'
        request_file = os.path.join(
            env.work_order_receipt,
            "work_order_receipt_lookup_success.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            env.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_workorder_receipt_lookup_response(receipt_response, operator.gt, 0)
                is ResultStatus.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

