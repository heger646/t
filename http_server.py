import os
import json
import base64
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import quote

HTTP_BASE_DIR = r"E:\web-server"
HTTP_IP = "192.168.8.19"
HTTP_PORT = 8080
SAVE_DIR = os.path.join(HTTP_BASE_DIR, "public", "drawings")
os.makedirs(SAVE_DIR, exist_ok=True)

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/save_png":
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            image_data = data["image"].split(",")[1]
            img_bytes = base64.b64decode(image_data)

            filename = f"drawing_{int(__import__('time').time())}.png"
            filepath = os.path.join(SAVE_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(img_bytes)

            url_path = f"/public/drawings/{filename}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"url": url_path}).encode())
        else:
            self.send_error(404, "Unknown endpoint")

    # Override directory listing
    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = quote(self.path)
        r.append('<html><head>')
        r.append(f'<title>Directory listing for {displaypath}</title>')
        r.append('</head><body>')
        r.append(f'<h2>Directory listing for {displaypath}</h2>')
        r.append('<hr><ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
            r.append(f'<li><a href="{quote(displayname)}">{displayname}</a></li>')
        r.append('</ul><hr></body></html>')
        encoded = '\n'.join(r).encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return

if __name__ == "__main__":
    os.chdir(HTTP_BASE_DIR)
    server = HTTPServer((HTTP_IP, HTTP_PORT), MyHandler)
    print(f"HTTP server running at http://{HTTP_IP}:{HTTP_PORT}/ serving {HTTP_BASE_DIR}")
    server.serve_forever()
