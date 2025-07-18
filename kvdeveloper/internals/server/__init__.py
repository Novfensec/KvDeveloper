import http.server
import os
import socket
import socketserver
import threading
from typing import List

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from kvdeveloper.config import console

changed_files = set()


class ChangeTrackerHandler(FileSystemEventHandler):
    def __init__(self, allowed_exts: List[str]) -> None:
        self.allowed_exts = allowed_exts

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory and any(
            event.src_path.endswith(ext) for ext in self.allowed_exts
        ):
            rel_path = os.path.relpath(event.src_path, os.getcwd()).replace("\\", os.sep)
            changed_files.add(rel_path)


class ExtensionFilterHandler(http.server.SimpleHTTPRequestHandler):
    """Serves only files with allowed extensions."""

    allowed_extensions: List[str] = []

    def do_GET(self) -> None:
        if self.path == "/changes.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            import json

            global changed_files
            self.wfile.write(json.dumps(list(changed_files)).encode("utf-8"))
            changed_files.clear()
            return

        if (
            self.path == "/"
            or self.path.endswith("/")
            or self.is_allowed_extension(self.path)
        ):
            super().do_GET()
        else:
            self.send_error(403, "Forbidden file type")

    def is_allowed_extension(self, path: str) -> bool:
        print(os.path.basename(path))
        return any(
            os.path.basename(path).endswith(ext) for ext in self.allowed_extensions
        )


class FileChangeLogger(FileSystemEventHandler):
    """Logs file changes in the directory."""

    def __init__(self, watch_dir: str, allowed_extensions: List[str]) -> None:
        self.watch_dir = watch_dir
        self.allowed_extensions = allowed_extensions

    def on_modified(self, event: FileSystemEvent) -> None:
        if any(event.src_path.endswith(ext) for ext in self.allowed_extensions):
            console.print(f"[MODIFIED] [bright_white]{event.src_path}[/bright_white]")

    def on_created(self, event: FileSystemEvent) -> None:
        if any(event.src_path.endswith(ext) for ext in self.allowed_extensions):
            console.print(f"[CREATED] [bright_green]{event.src_path}[/bright_green]")

    def on_deleted(self, event: FileSystemEvent) -> None:
        if any(event.src_path.endswith(ext) for ext in self.allowed_extensions):
            console.print(f"[DELETED] [bright_red]{event.src_path}[/bright_red]")


def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


local_ip = get_ip_address()


class LocalFileServer:
    def __init__(
        self,
        directory: str = ".",
        port: int = 8000,
        extensions: List[str] | None = None
    ) -> None:
        self.directory = os.path.abspath(directory)
        self.port = port
        self.extensions = extensions or [
            ".kv", ".py", ".txt", ".png", ".jpg", ".atlas", ".toml"
        ]
        self.httpd = None
        self.observer = None

    def start_server(self) -> None:
        os.chdir(self.directory)

        ExtensionFilterHandler.allowed_extensions = self.extensions
        handler = ExtensionFilterHandler
        self.httpd = socketserver.TCPServer((local_ip, self.port), handler)

        console.print(f"Serving on [bright_white]http://{local_ip}:{self.port}[/bright_white] (only {self.extensions})\n")
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def start_watcher(self) -> None:
        console.print(f"Watching [bright_white]'{self.directory}'[/bright_white] for changes...")
        event_handler = ChangeTrackerHandler(self.extensions)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()

    def run(self) -> None:
        try:
            self.start_server()
            self.start_watcher()
            while True:
                pass  # Keep main thread alive
        except KeyboardInterrupt:
            print("\nShutting down server and watcher...")
            self.httpd.shutdown()
            self.observer.stop()
            self.observer.join()


# === Example usage ===
if __name__ == "__main__":
    server = LocalFileServer(
        directory="./MyApp", port=8000, extensions=[".kv", ".py", ".txt"]
    )
    server.run()
