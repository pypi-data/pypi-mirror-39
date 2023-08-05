'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''


import sys
import socket
import os

import traffic_replay.Scheduler as Scheduler
import traffic_replay.glb as glb


def check_for_ats(hostname, port):
    ''' Checks to see if ATS is running on `hostname` and `port`
    If not running, this function will terminate the script
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((hostname, port))
    if result != 0:
        # hostname:port is not being listened to
        print('==========')
        print('Error: Apache Traffic Server is not running on {0}:{1}'.format(
            hostname, port))
        print('Aborting')
        print('==========')
        sys.exit()
# Note: this function can't handle multi-line (ie wrapped line) headers
# Hopefully this isn't an issue because multi-line headers are deprecated now


def main(path, replay_type, Bverbose, pHost=glb.proxy_host, pNSSLport=glb.proxy_nonssl_port, pSSL=glb.proxy_ssl_port):
    check_for_ats(pHost, pNSSLport)
    glb.proxy_host = pHost
    glb.proxy_nonssl_port = pNSSLport
    glb.proxy_ssl_port = pSSL
    proxy = {
        "http": "http://{0}:{1}".format(glb.proxy_host, glb.proxy_nonssl_port)}
    Scheduler.LaunchWorkers(path, glb.nProcess, proxy,
                            replay_type, glb.nThread)
