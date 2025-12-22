#!/usr/bin/env python3
"""Smoke-test a built engine artifact (exe or binary).

Usage: python scripts/smoke_test_artifact.py /path/to/executable

The script starts the engine process, sends a few UCI commands, and checks basic responses.
"""
import sys
import subprocess
import time


def run_smoke(exe_path: str, timeout: int = 10) -> bool:
    try:
        proc = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"Failed to start {exe_path}: {e}")
        return False

    def send(cmd: str):
        proc.stdin.write(cmd + "\n")
        proc.stdin.flush()

    # Give the engine a moment to start
    time.sleep(0.2)
    send("uci")

    got_uciok = False
    start = time.time()
    while time.time() - start < timeout:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        print("OUT:", line)
        if line == "uciok":
            got_uciok = True
            break

    if not got_uciok:
        print("Did not get 'uciok' from engine")
        proc.kill()
        return False

    send("isready")
    got_ready = False
    start = time.time()
    while time.time() - start < timeout:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        print("OUT:", line)
        if line == "readyok":
            got_ready = True
            break

    if not got_ready:
        print("Did not get 'readyok' from engine")
        proc.kill()
        return False

    # Run a quick search
    send("position startpos")
    send("go depth 1")

    got_best = False
    start = time.time()
    while time.time() - start < timeout:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        print("OUT:", line)
        if line.startswith("bestmove"):
            got_best = True
            break

    proc.kill()
    if not got_best:
        print("Did not get 'bestmove' from engine")
        return False

    print("Smoke test succeeded")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: scripts/smoke_test_artifact.py /path/to/executable")
        sys.exit(2)
    ok = run_smoke(sys.argv[1])
    sys.exit(0 if ok else 3)
