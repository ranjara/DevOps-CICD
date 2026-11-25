from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "application": "cicd-demo"
            }
        else:
            response = {
                "message": "Hello! My first CI/CD application is running.",
                "version": "1.0"
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def run_server():
    server = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Application running on port 5000")
    server.serve_forever()


if __name__ == "__main__":
    run_server()