import json
import random
import socket
from typing import Iterator, List  # noqa

from .types import Attachment, Message


def readlines(s: socket.socket) -> Iterator[bytes]:
    "Read a socket, line by line."
    buf = []  # type: List[bytes]
    while True:
        char = s.recv(1)
        if not char:
            raise ConnectionResetError("connection was reset")

        if char == b"\n":
            yield b"".join(buf)
            buf = []
        else:
            buf.append(char)


class Signal:
    def __init__(self, username, socket_path="/var/run/signald/signald.sock"):
        self.username = username
        self.socket_path = socket_path

    def _get_id(self):
        "Generate a random ID."
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(10))

    def _get_socket(self) -> socket.socket:
        "Create a socket, connect to the server and return it."
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)
        return s

    def _send_command(self, payload: dict, block: bool = False):
        s = self._get_socket()
        msg_id = self._get_id()
        payload["id"] = msg_id
        s.recv(1024)  # Flush the buffer.
        s.send(json.dumps(payload).encode("utf8") + b"\n")

        if not block:
            return

        response = s.recv(4 * 1024)
        for line in response.split(b"\n"):
            if msg_id.encode("utf8") not in line:
                continue

            data = json.loads(line)

            if data.get("id") != msg_id:
                continue

            if data["type"] == "unexpected_error":
                raise ValueError("unexpected error occurred")

    def register(self, voice=False):
        """
        Register the given number.

        voice: Whether to receive a voice call or an SMS for verification.
        """
        payload = {"type": "register", "username": self.username, "voice": voice}
        self._send_command(payload)

    def verify(self, code: str):
        """
        Verify the given number by entering the code you received.

        code: The code Signal sent you.
        """
        payload = {"type": "verify", "username": self.username, "code": code}
        self._send_command(payload)

    def receive_messages(self) -> Iterator[Message]:
        "Keep returning received messages."
        s = self._get_socket()
        s.send(json.dumps({"type": "subscribe", "username": self.username}).encode("utf8") + b"\n")

        for line in readlines(s):
            try:
                message = json.loads(line.decode())
            except json.JSONDecodeError:
                print("Invalid JSON")

            if message.get("type") != "message":
                continue

            message = message["data"]

            yield Message(
                username=message["username"],
                source=message["source"],
                message=message["dataMessage"]["message"],
                source_device=message["sourceDevice"],
                timestamp=message["dataMessage"]["timestamp"],
                timestamp_iso=message["timestampISO"],
                expiration_secs=message["dataMessage"]["expiresInSeconds"],
                attachments=[
                    Attachment(
                        content_type=attachment["contentType"],
                        id=attachment["id"],
                        size=attachment["size"],
                        stored_filename=attachment["storedFilename"],
                    )
                    for attachment in message["dataMessage"]["attachments"]
                ],
            )

    def send_message(self, recipient: str, message: str, block: bool = True) -> None:
        """
        Send a message.

        recipient: The recipient's phone number, in E.123 format.
        message:   The message to send.
        block:     Whether to block while sending. If you choose not to block, you won't get an exception if there
                   are any errors.
        """
        payload = {"type": "send", "username": self.username, "recipientNumber": recipient, "messageBody": message}
        self._send_command(payload, block)
