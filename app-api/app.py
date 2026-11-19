# app-api : เอาข้อความหลัง /api/ มาแสดงตัวใหญ่กลางจอ
import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path.startswith("/api/") and len(path) > 5:
            msg = unquote(path[5:])
        else:
            msg = "ใส่ข้อความต่อท้าย /api/ เช่น /api/hello"
        text = f"""<!doctype html><html><head><meta charset="utf-8"><title>API</title>
<style>body{{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;font-family:Tahoma,sans-serif}}
h1{{font-size:80px;text-align:center;word-break:break-all}}</style></head>
<body><h1>{html.escape(msg)}</h1></body></html>"""
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Pod-Name", os.environ.get("HOSTNAME", ""))
        self.end_headers()
        self.wfile.write(data)


print("app-api running on port 8080")
ThreadingHTTPServer(("", 8080), Handler).serve_forever()
