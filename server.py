# server.py
from jsonrpcserver import methods
from jsonrpcserver.response import HTTPResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import middleware
import config

# Placeholder function to handle JSON-RPC methods
@methods.add
def example_method(param1, param2):
    # Placeholder logic for the JSON-RPC method
    result = param1 + param2
    return result

# Implement other JSON-RPC methods here

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')
            response = middleware.handle_request(request_body)
        except Exception as e:
            response = HTTPResponse(str(e), status=500)
            
        self.send_response(response.http_status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.body.encode('utf-8'))

def serve():
    server = HTTPServer((config.SERVER_ADDRESS, config.SERVER_PORT), RequestHandler)
    logging.info('Starting JSON-RPC server...')
    server.serve_forever()

if __name__ == '__main__':
    logging.basicConfig(level=config.LOGGING_LEVEL)
    serve()
