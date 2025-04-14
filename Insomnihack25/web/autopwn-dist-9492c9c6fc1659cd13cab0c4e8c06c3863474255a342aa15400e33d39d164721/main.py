from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)  # Use 302 for a temporary redirect
        self.send_header("Location", "https://autopwn.insomnihack.ch/")
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RedirectHandler, port=1337):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port} and redirecting to Google...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
