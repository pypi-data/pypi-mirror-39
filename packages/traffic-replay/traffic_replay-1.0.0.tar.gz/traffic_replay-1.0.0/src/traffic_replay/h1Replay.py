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

import socket
import sys
import ssl
import http.client
from traceback import print_exc
from threading import Thread

import trlib.result as result

import traffic_replay.extractHeader as extractHeader
import traffic_replay.glb as glb

bSTOP = False


class ProxyHTTPSConnection(http.client.HTTPSConnection):
    "This class allows communication via SSL."

    default_port = http.client.HTTPS_PORT

    # XXX Should key_file and cert_file be deprecated in favour of context?

    def __init__(self, host, port=None, key_file=None, cert_file=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 source_address=None, *, context=None,
                 check_hostname=None, server_name=None):
        # http.client.HTTPSConnection.__init__(self)
        super().__init__(host, port, key_file, cert_file, timeout,
                         source_address, context=context, check_hostname=check_hostname)
        '''
            self.key_file = key_file
            self.cert_file = cert_file
            if context is None:
                context = ssl._create_default_https_context()
            will_verify = context.verify_mode != ssl.CERT_NONE
            if check_hostname is None:
                check_hostname = context.check_hostname
            if check_hostname and not will_verify:
                raise ValueError("check_hostname needs a SSL context with "
                                 "either CERT_OPTIONAL or CERT_REQUIRED")
            if key_file or cert_file:
                context.load_cert_chain(cert_file, key_file)
            self._context = context
            self._check_hostname = check_hostname
            '''
        self.server_name = server_name

    def connect(self):
        "Connect to a host on a given (SSL) port."
        http.client.HTTPConnection.connect(self)

        if self._tunnel_host:
            server_hostname = self._tunnel_host
        else:
            server_hostname = self.server_name
        self.sock = self._context.wrap_socket(self.sock,
                                              do_handshake_on_connect=True,
                                              server_side=False,
                                              server_hostname=server_hostname)
        if not self._context.check_hostname and self._check_hostname:
            try:
                ssl.match_hostname(self.sock.getpeercert(), server_hostname)
            except Exception:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                raise


def createDummyBodywithLength(numberOfbytes):
    if numberOfbytes <= 0:
        return None
    body = 'a'
    while numberOfbytes != 1:
        body += 'b'
        numberOfbytes -= 1
    return body


def handleResponse(response, *args, **kwargs):
    print(response.status_code)
    # resp=args[0]
    #expected_output_split = resp.getHeaders().split('\r\n')[ 0].split(' ', 2)
    #expected_output = (int(expected_output_split[1]), str( expected_output_split[2]))
    #r = result.Result(session_filename, expected_output[0], response.status_code)
    # print(r.getResultString(colorize=True))
# make sure len of the message body is greater than length


def gen():
    yield 'pforpersia,champaignurbana'.encode('utf-8')
    yield 'there'.encode('utf-8')


def txn_replay(session_filename, txn, proxy, result_queue, session_conn):
    req = txn.getClientRequest()
    resp = txn.getProxyResponse()

    # Construct HTTP(S) request & fire it off
    txn_req_headers = req.getHeaders()
    # print(txn_req_headers)

    if 'body' in txn_req_headers:
        del txn_req_headers['body']

    try:
        method = req.getMethod()
        response = None
        body = None
        content = None
        if 'Transfer-Encoding' in txn_req_headers:
            # deleting the host key, since the STUPID post/get functions are going to add host field anyway, so there will be multiple host fields in the header
            # This confuses the ATS and it returns 400 "Invalid HTTP request". I don't believe this
            # BUT, this is not a problem if the data is not chunked encoded.. Strange, huh?
            del txn_req_headers['Host']
            if 'Content-Length' in txn_req_headers:
                #print("ewww !")
                del txn_req_headers['Content-Length']
            body = gen()
        if 'Content-Length' in txn_req_headers:
            nBytes = int(txn_req_headers['Content-Length'])
            body = createDummyBodywithLength(nBytes)

        # print("sending {0} {1} {2}".format(method, req.getURL(), txn_req_headers))
        print("sending {0}".format(method))

        session_conn.request(method, req.getURL(), headers=txn_req_headers,
                             body=body, encode_chunked='Transfer-Encoding' in txn_req_headers)

        r1 = session_conn.getresponse()
        responseContent = r1.read(resp.getContentSize())  # NOTE: is this ok?
        responseHeaders = extractHeader.responseHeaderTuple_to_dict(
            r1.getheaders())

        expected_headers = resp.getHeaders()

        if glb.verify:
            r = result.Result(session_filename, resp.getStatus(),
                              r1.status, responseContent)
            b_res, res = r.getResult(
                responseHeaders, resp.getHeaders(), colorize=glb.colorize)
            print(res)

            if not b_res:
                print("TXN UUID: {0}".format(txn_req_headers['uuid']))
                print("Received response")
                print(responseHeaders)
                print("Expected response")
                print(resp.getHeaders())
        # result_queue.put(r)
    # except UnicodeEncodeError as e:
    #     # these unicode errors are due to the interaction between Requests and our wiretrace data.
    #     # TODO fix
    #     print("UnicodeEncodeError exception")
    # except http.client.IncompleteRead as e:
    #     print("INCOMPLETE READ ERROR")
    #     print(e.partial)
    except Exception as e:
        # e = sys.exc_info()
        print("Error in txn UUID {0} method {1} url {2}".format(
            txn_req_headers['uuid'], method, req.getURL()))
        print_exc()
        raise
        # print("ERROR in replaying: ", e, response, session_filename)


def session_replay(input, proxy, result_queue, isSsl):
    global bSTOP
    ''' Replay all transactions in session 
    
    This entire session will be replayed in one http.client.HTTP(S)Connection (so one socket / TCP connection)'''

    while bSTOP == False:
        for session in iter(input.get, 'STOP'):
            if session == 'STOP':
                print("Queue is empty")
                bSTOP = True
                break

            conn = None

            if isSsl:
                req = session.getFirstTransaction().getClientRequest()
                # Construct HTTP request & fire it off
                txn_req_headers = req.getHeaders()
                sc = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
                sc.load_cert_chain(glb.ca_certs, keyfile=glb.keyfile)
                conn = ProxyHTTPSConnection(glb.proxy_host, glb.proxy_ssl_port, cert_file=glb.ca_certs,
                                            key_file=glb.keyfile, context=sc, server_name=txn_req_headers['Host'])
            else:
                conn = http.client.HTTPConnection(
                    glb.proxy_host, port=glb.proxy_nonssl_port)

            for txn in session.getTransactionIter():
                try:
                    txn_replay(session._filename, txn,
                               proxy, result_queue, conn)
                except:
                    e = sys.exc_info()
                    print("ERROR in replaying: ", e,
                          txn.getClientRequest().getHeaders())

                    if isSsl:
                        conn = ProxyHTTPSConnection(glb.proxy_host, glb.proxy_ssl_port, cert_file=glb.ca_certs,
                                                    key_file=glb.keyfile, context=sc, server_name=txn_req_headers['Host'])
                    else:
                        conn = http.client.HTTPConnection(
                            glb.proxy_host, port=glb.proxy_nonssl_port)

        bSTOP = True
        #print("Queue is empty")
        input.put('STOP')
        break


def client_replay(input, proxy, result_queue, nThread, isSsl):
    Threads = []
    for _ in range(nThread):
        t = Thread(target=session_replay, args=[
                   input, proxy, result_queue, isSsl])
        t.start()
        Threads.append(t)

    for t1 in Threads:
        t1.join()
