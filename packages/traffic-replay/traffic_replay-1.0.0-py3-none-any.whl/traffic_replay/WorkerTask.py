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

from multiprocessing import current_process

# import traffic_replay.h2Replay as h2Replay
import traffic_replay.h1Replay as h1Replay


def worker(input, output, proxy, replay_type, nThread):
    h1Replay.client_replay(input, proxy, output,
                           nThread, replay_type == 'ssl')

    # h2 commented out because h2replay will be implemented at a later date

    # if replay_type == 'h2':
    #     h2Replay.client_replay(input, proxy, output, nThread)
    # else:
    #     h1Replay.client_replay(input, proxy, output,
    #                            nThread, replay_type == 'ssl')

    print("process{0} has exited".format(current_process().name))
