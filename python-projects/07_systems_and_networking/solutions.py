"""
Module 07: Systems and Networking — Solutions
"""
import socket
import subprocess
import re
import argparse
import json
from pathlib import Path
from typing import Optional


# --- Socket programming ---

def tcp_echo_server(host: str = "127.0.0.1", port: int = 0) -> tuple[str, int]:
    """Start a simple TCP echo server. Returns (host, port).
    Use port=0 to get an OS-assigned port.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    actual_port = server.getsockname()[1]
    server.listen(1)

    def handle():
        conn, _ = server.accept()
        with conn:
            data = conn.recv(1024)
            conn.sendall(data)  # echo back
        server.close()

    import threading
    t = threading.Thread(target=handle, daemon=True)
    t.start()
    return host, actual_port


def tcp_client_send(host: str, port: int, message: str) -> str:
    """Send a message to a TCP server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        return s.recv(1024).decode()


# --- HTTP from scratch ---

def http_get(host: str, path: str = "/", port: int = 80) -> dict:
    """Minimal HTTP/1.0 GET over raw socket. Returns status, headers, body."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((host, port))
        request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    raw = response.decode("utf-8", errors="replace")
    header_part, _, body = raw.partition("\r\n\r\n")
    lines = header_part.split("\r\n")
    status_line = lines[0]  # e.g. "HTTP/1.0 200 OK"
    status_code = int(status_line.split()[1])
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    return {"status": status_code, "headers": headers, "body": body}


# --- Subprocess management ---

def run_command(cmd: list[str], timeout: int = 10) -> dict:
    """Run a shell command and return stdout, stderr, returncode."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "timeout", "returncode": -1}
    except FileNotFoundError:
        return {"stdout": "", "stderr": f"command not found: {cmd[0]}", "returncode": 127}


# --- Regex patterns ---

def extract_ips(text: str) -> list[str]:
    """Extract all IPv4 addresses from text."""
    pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    return re.findall(pattern, text)


def extract_emails(text: str) -> list[str]:
    """Extract all email addresses from text."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(pattern, text)


def parse_log_line(line: str) -> Optional[dict]:
    """Parse Apache combined log format.
    Example: 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
    """
    pattern = (
        r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
    )
    m = re.match(pattern, line)
    if not m:
        return None
    return {
        "ip": m.group("ip"),
        "time": m.group("time"),
        "method": m.group("method"),
        "path": m.group("path"),
        "status": int(m.group("status")),
        "size": m.group("size"),
    }


# --- File system operations ---

def find_files(root: str, pattern: str = "*.py") -> list[Path]:
    """Find all files matching glob pattern under root."""
    return list(Path(root).rglob(pattern))


def read_config(path: str) -> dict:
    """Read JSON config file with defaults."""
    defaults = {"debug": False, "port": 8080, "host": "0.0.0.0"}
    try:
        with open(path) as f:
            user_config = json.load(f)
        return {**defaults, **user_config}  # user settings override defaults
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults


# --- Argument parsing ---

def build_parser() -> argparse.ArgumentParser:
    """Build a CLI argument parser for a hypothetical network scanner."""
    parser = argparse.ArgumentParser(description="Network utility tool")
    parser.add_argument("target", help="Target host or IP")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port (default: 80)")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--output", choices=["text", "json", "csv"], default="text")
    return parser


if __name__ == "__main__":
    # Echo server/client
    host, port = tcp_echo_server()
    response = tcp_client_send(host, port, "hello")
    assert response == "hello"

    # Command runner
    result = run_command(["echo", "test"])
    assert result["returncode"] == 0
    assert "test" in result["stdout"]

    # Regex
    text = "Connect from 192.168.1.1 and 10.0.0.2 to server"
    ips = extract_ips(text)
    assert "192.168.1.1" in ips and "10.0.0.2" in ips

    emails_text = "Contact admin@example.com or support@test.org"
    emails = extract_emails(emails_text)
    assert "admin@example.com" in emails

    # Log parsing
    log = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326'
    parsed = parse_log_line(log)
    assert parsed["ip"] == "127.0.0.1"
    assert parsed["status"] == 200
    assert parsed["path"] == "/index.html"

    # Config
    cfg = read_config("/nonexistent.json")
    assert cfg["port"] == 8080

    print("All assertions passed.")
