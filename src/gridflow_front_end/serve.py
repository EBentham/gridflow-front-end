"""gridflow-serve — one-command local server for the Gridflow static site.

Usage:
    gridflow-serve              # port 8765, opens browser automatically
    gridflow-serve --port 9000  # custom port
    gridflow-serve --no-open    # skip browser launch
"""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
import webbrowser

from gridflow_front_end.paths import SITE_DIR


class _SilentHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler without the per-request log lines; real errors still print."""

    def log_message(self, format: str, *args: object) -> None:
        pass

    def log_error(self, format: str, *args: object) -> None:
        sys.stderr.write(f"[gridflow-serve] ERROR: {format % args}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gridflow-serve", description="Serve the Gridflow static site locally."
    )
    parser.add_argument("--port", type=int, default=8765, help="TCP port (default: 8765)")
    parser.add_argument("--no-open", action="store_true", help="Do not open a browser tab")
    args = parser.parse_args()

    if not SITE_DIR.is_dir():
        sys.exit(f"[gridflow-serve] Site directory not found: {SITE_DIR}")
    handler = functools.partial(_SilentHandler, directory=str(SITE_DIR))
    try:
        # Threading, not http.server.HTTPServer: SimpleHTTPRequestHandler speaks HTTP/1.1
        # keep-alive, so one idle browser connection would hold a single-threaded server's only
        # handler and every other request would wait until it timed out.
        server = http.server.ThreadingHTTPServer(("", args.port), handler)
    except OSError as exc:
        sys.exit(
            f"[gridflow-serve] Could not bind to port {args.port}: {exc}\n"
            "Try a different port with --port <number>."
        )

    url = f"http://localhost:{args.port}/"
    print(f"Gridflow  ·  serving on {url}")
    print("Press Ctrl+C to stop.\n")
    if not args.no_open:
        # the socket is bound and listening, so the browser's request waits for serve_forever
        webbrowser.open(url)
    with server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[gridflow-serve] Stopped.")


if __name__ == "__main__":
    main()
