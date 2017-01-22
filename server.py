#  coding: utf-8 
import SocketServer, os, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Sarah Morris
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        response = self.getResponse()

        self.request.sendall(response)

    def getResponse(self):

        # make sure the method of the request is a GET
        if not self.check_method():
            return self.bad_method()

        # parse the path
        return self.get_path()


    def check_method(self):
        method = self.data.split(' ', 1)
        if method[0] != "GET":
            return False
        else:
            return True

    def bad_method(self):
        status = "405 Method Not Allowed\r\n"
        connection = "Connection: close\r\n"
        return status

    def get_path(self):
        
        # extract the path from the request
        path = self.data.split(' ', 2)[1]

        # check if path has www already
        if path.split("/", 1)[0] != 'www':
            path = "www/" + path
        
        # get rid of any '..'
        path = os.path.abspath(path)

        # check if the path is a directory or a file
        if os.path.isdir(path): 
            path = path + "/index.html"

        # make sure the file exists and is in the www directory
        if os.path.isfile(path) and ("www" in path):
            return self.ok(path)
        else:
            return self.not_found()

    def not_found(self):
        # returns 404 not found response
        status = "HTTP/1.1 404 Not Found\r\n"
        contentType = "text/html\r\n"
        connection = "Connection: close\r\n"

        body = open("404.html", 'r').read()

        return status + contentType + connection + "\r\n" + body

    def ok(self, path):
        # returns a 200 OK
        status = "HTTP/1.1 200 OK\r\n"

        # get the content length
        fileSize = os.path.getsize(path)
        contentLength = "Content-Length: " + str(fileSize) + "\r\n"

        contentType = "Content-Type: " + mimetypes.guess_type(path)[0] + "\r\n"

        connection = "Connection: close \r\n"

        body = open(path, 'r').read()

        return status + contentType + connection + "\r\n" + body + "\r\n"

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
