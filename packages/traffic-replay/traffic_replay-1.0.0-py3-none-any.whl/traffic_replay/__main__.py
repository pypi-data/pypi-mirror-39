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

import argparse

import traffic_replay.mainProcess as mainProcess
import traffic_replay.glb as glb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", "-t", type=str,
                        help="Replay type: ssl/nossl/mixed (at least 2 processes needed for mixed)")
    # help="Replay type: ssl/random/h2/nossl/mixed (at least 2 processes needed for mixed)")

    parser.add_argument("--log_dir", "-l", type=str, required=True,
                        help="directory of JSON replay files")

    parser.add_argument("--verify", action="store_true",
                        help="verify response status code")

    parser.add_argument("--host", "-H", default=glb.proxy_host,
                        help="proxy/host IP to send the requests to (default: 127.0.0.1)")

    parser.add_argument("--port", "-p", type=int, default=glb.proxy_nonssl_port,
                        help="The non secure port of ATS to send the request to (default: 8080)")

    parser.add_argument("--s_port", "-s", type=int, default=glb.proxy_ssl_port,
                        help="The secure port of ATS to send the request to (default: 12345)")

    parser.add_argument("--ca_cert", "-c", default=glb.ca_certs,
                        help="Certificate to present")

    parser.add_argument("--key", "-k", default=glb.keyfile,
                        help="Key for ssl connection")

    parser.add_argument("--colorize", action="store_true", default=glb.colorize,
                        help="specify whether to use colorize the output")

    args = parser.parse_args()

    # Let 'er loose
    #main(args.log_dir, args.hostname, int(args.port), args.threads, args.timing, args.verbose)
    glb.colorize = args.colorize
    glb.verify = args.verify
    glb.keyfile = args.key
    glb.ca_certs = args.ca_cert

    mainProcess.main(args.log_dir, args.type, glb.verify,
                     pHost=args.host, pNSSLport=args.port, pSSL=args.s_port)


if __name__ == '__main__':
    main()
