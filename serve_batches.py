import http.server
import os

os.chdir(r'c:\Thesis_Hr_system\humanize_chunks_450')

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    def log_message(self, *a):
        pass

server = http.server.HTTPServer(('127.0.0.1', 9876), CORSHandler)
print('SERVER_READY on port 9876')
server.serve_forever()
