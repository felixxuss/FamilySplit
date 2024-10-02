import os


def stprint(text: str):
    os.write(1, f"{text}\n".encode())
