#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path


class Utf8StaticHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        content_type = super().guess_type(path)
        suffix = Path(path).suffix.lower()
        if suffix in {".html", ".htm", ".md", ".txt", ".css", ".js", ".json", ".ipynb"}:
            base_type = {
                ".md": "text/markdown",
                ".txt": "text/plain",
                ".css": "text/css",
                ".js": "application/javascript",
                ".json": "application/json",
                ".ipynb": "application/x-ipynb+json",
            }.get(suffix, "text/html")
            return f"{base_type}; charset=utf-8"
        if content_type.startswith("text/") and "charset=" not in content_type:
            return f"{content_type}; charset=utf-8"
        return content_type


def main():
    host = os.environ.get("AMSL_STUDY_HOST", "127.0.0.1")
    port = int(os.environ.get("AMSL_STUDY_PORT", "8767"))
    root = Path(os.environ.get("AMSL_STUDY_ROOT", Path(__file__).resolve().parent)).resolve()
    handler = lambda *args, **kwargs: Utf8StaticHandler(*args, directory=str(root), **kwargs)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving {root} on http://{host}:{port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
