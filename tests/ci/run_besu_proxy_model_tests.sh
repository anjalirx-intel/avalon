#! /bin/bash

# Copyright 2020 Intel Corporation
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

yell() {
    echo "$0: $*" >&2;
}

die() {
    yell "$*"
    exit 111
}

try() {
    "$@" || die "test failed: $*"
}

# In minifab is instantiating worker chain code in one of peer.
# If worker chain code call goes to other peer then fresh instantiation will take some
# time, so run test will wait for about 1min.

yell "Wait for Ethereum blockchain connector to register worker"
sleep 60s

SCRIPTDIR="$(dirname $(readlink --canonicalize ${BASH_SOURCE}))"
SRCDIR="$(realpath ${SCRIPTDIR}/..)"
automation_test_path="${TCF_HOME}/tests/automation_framework"
generic_client_path="${TCF_HOME}/examples/apps/generic_client"

yell "Start testing Ethereum generic client for echo result workload ................"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py -b ethereum \
        --workload_id "echo-result" \
        --in_data "Hello Fabric proxy model" -o

yell "Start testing fabric generic client for heart disease eval workload ................"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py -b ethereum \
        --workload_id "heart-disease-eval" \
        --in_data "Data: 25 10 1 67  102 125 1 95 5 10 1 11 36 1" -o

yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"
yell "Start Generic client Tests  ................"
yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"






yell "QCID_18393_Test Workorder success for echo-client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "Hello" -o

yell "QCID_18402_Test Workorder success for heart-disease-eval workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" \
    --in_data "Data: 25 10 1 67  102 125 1 95 5 10 1 11 36 1" -o

yell "QCID_18404_Test special character for heart disease eval workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" \
    --in_data "Data: 25 10 1 67  102 125 1 95 * & ! @ # %" -o
yell "Test Completed"

yell "QCID_18396_Test alpha numeric characters for echo client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "Hello12345" -o
yell "Test Completed"

yell "QCID_18397_Test workorder only digits for echo client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "12345678" -o
yell "Test Completed"

yell "QCID_18395_Test workorder only spaces for echo client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "     " -o
yell "Test Completed"

yell "QCID_18403_Test workorder only special character for heart disease eval workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" \
    --in_data "Data: $ @ ! %  ^ & * # * & ! @ # %" -o
yell "Test Completed"

yell "QCID_18406_Test workorder by passing paragraph for echo client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "JMeter is a performance test tool. So it runs in parallel using multi-threading. However you can also use just 1 thread group and set the thread count to one to run it in sequence" -o
yell "Test Completed"

yell "QCID_18394_Test workorder special character payload for echo client workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "#@!$%@#&*()$%#" -o
yell "Test Completed"

yell "QCID_18430_Test Workorder indata by passing negative value for heart-disease-eval workload"
yell "#------------------------------------------------------------------------------------------------"
try $generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" \
    --in_data "Data: 25 10 1 67  102 125 1 95 5 10 1 11 36 -1" -o
yell "Test Completed"

yell "QCID_20315_Test Workorder with empty indata for heart-disease-eval workload"
yell "#------------------------------------------------------------------------------------------------"
$generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" --in_data "" -o
yell "Test Completed"

yell "QCID_20318_Test Workorder with requester signature echo-client workload"
yell "#------------------------------------------------------------------------------------------------"
$generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "echo-result" --in_data "Hello" -o --requester_signature
yell "Test Completed"

yell "QCID_20319_Test Workorder with requester signature for heart-disease-eval workload"
yell "#------------------------------------------------------------------------------------------------"
$generic_client_path/eth_generic_client.py --blockchain ethereum \
    --workload_id "heart-disease-eval" \
    --in_data "Data: 25 10 1 67  102 125 1 95 5 10 1 11 36 1" -o \
    --requester_signature
yell "Test Completed"


yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"

yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"
yell "Start Automated Tests  ................"
yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"

# cd ${TCF_HOME}/tests/automation_framework
# mkdir /project/avalon/logs
# echo `pwd`
#pytest -m "sdk" --junitxml /project/avalon/logs/eth_besu_proxy_results.xml \
#    2>&1 | tee /project/avalon/logs/eth_besu_proxy_logs.txt

yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"

yell completed all tests
yell "#------------------------------------------------------------------------------------------------"
yell "#------------------------------------------------------------------------------------------------"

exit 0
