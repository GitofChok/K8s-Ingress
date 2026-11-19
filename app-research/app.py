# app-research : แสดงสรุปงานวิจัยที่ /research และหน้าแก้ไขที่ /edit
import html
import os
import shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

DATA_FILE = "/data/research.txt"
FIRST_FILE = "/app/research.txt"
DOMAIN = os.environ.get("DOMAIN", "id-594.com")

if not os.path.exists(DATA_FILE):
    shutil.copy(FIRST_FILE, DATA_FILE)


def load():
    with open(DATA_FILE, encoding="utf-8") as f:
        return f.read()


def page(title, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>body{{font-family:Tahoma,sans-serif;max-width:850px;margin:30px auto;padding:0 15px;line-height:1.7}}
textarea{{width:100%;height:480px;font-size:15px}} button{{font-size:16px;padding:6px 20px}}</style>
</head><body>{body}<hr><small>pod: {os.environ.get('HOSTNAME')}</small></body></html>"""


def show_research():
    parts = [p.strip() for p in load().split("\n\n") if p.strip()]
    body = f"<h1>{html.escape(parts[0])}</h1>"
    for p in parts[1:]:
        lines = p.split("\n")
        if len(lines) > 1 and len(lines[0]) < 40:
            body += f"<h3>{html.escape(lines[0])}</h3>"
            lines = lines[1:]
        body += "<p>" + "<br>".join(html.escape(x) for x in lines) + "</p>"
    return page("Research", body)


def show_edit(msg=""):
    body = f"""<h1>แก้ไขสรุปงานวิจัย</h1>{msg}
<form method="post" action="/edit">
<textarea name="text">{html.escape(load())}</textarea><br><br>
<button type="submit">บันทึก</button>
</form>
<p><a href="http://www.{DOMAIN}/research">ดูหน้า research</a></p>"""
    return page("Edit research", body)


class Handler(BaseHTTPRequestHandler):
    def send(self, code, text):
        data = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/research", "/research/"):
            self.send(200, show_research())
        elif path in ("/edit", "/edit/"):
            self.send(200, show_edit())
        else:
            self.send(404, page("404", "<h1>404 not found</h1>"))

    def do_POST(self):
        if self.path.split("?")[0] not in ("/edit", "/edit/"):
            self.send(404, page("404", "<h1>404 not found</h1>"))
            return
        size = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(size).decode("utf-8"))
        text = form.get("text", [""])[0].replace("\r\n", "\n").strip() + "\n"
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        self.send(200, show_edit("<p style='color:green'><b>บันทึกเรียบร้อยแล้ว</b></p>"))


print("app-research running on port 8080")
ThreadingHTTPServer(("", 8080), Handler).serve_forever()
