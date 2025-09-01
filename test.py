import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import boto3

# Initialize S3 client
s3 = boto3.client("s3")
BUCKET_NAME = "aws23bps"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Add CORS headers for all POST requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000') # <--- Add this header
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        if self.path == '/upload':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                # Use cgi.FieldStorage to handle the entire form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             'CONTENT_LENGTH': self.headers['Content-Length']
                             })

                if 'files' in form and form['files'].filename:
                    file_item = form['files']
                    filename = os.path.basename(file_item.filename)
                    file_content = file_item.file.read()
                    
                    with open(filename, "wb") as f:
                        f.write(file_content)

                    s3.upload_file(filename, BUCKET_NAME, filename)
                    os.remove(filename)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'File uploaded and sent to S3 successfully')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid request: "files" field not found or is not a file')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid request')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000, bind="0.0.0.0"):
    server_address = (bind, port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on {bind} port {port} (http://{bind}:{port}/) ...")
    httpd.serve_forever()

if __name__ == "__main__":
    run(bind="0.0.0.0", port=8000)
