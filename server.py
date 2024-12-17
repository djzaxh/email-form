import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import database

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def serve_html(self, filename):
        """Helper method to read and serve an HTML file."""
        try:
            with open(os.path.join('templates', filename), 'rb') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            self.send_error(404, "Page Not Found")
            return None

    def do_GET(self):
        # Serve different HTML files based on the URL path
        if self.path == "/form":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content = self.serve_html('form.html')
            if content:
                self.wfile.write(content)
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content = self.serve_html('about.html')
            if content:
                self.wfile.write(content)
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            name = post_data.get('name', [''])[0]
            email = post_data.get('email', [''])[0]
            message = post_data.get('message', [''])[0]

            database.store_data(name, email, message)

            with open(os.path.join('templates', 'thank_you.html'), 'r') as file:
                response_html = file.read()
                response_html = response_html.replace('{{name}}', name)
                response_html = response_html.replace('{{email}}', email)
                response_html = response_html.replace('{{message}}', message)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response_html.encode('utf-8'))

if __name__ == "__main__":
    database.init_db()  # Initialize the database before starting the server
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()