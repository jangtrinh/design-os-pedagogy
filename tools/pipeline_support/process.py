"""Bounded provider process, draining both streams before waiting."""
import os
import signal
import subprocess
import threading
import math


def run_provider(command, prompt, timeout=180, max_bytes=2097152):
    if (not isinstance(command, (list, tuple)) or not command
            or any(not isinstance(arg, str) for arg in command)
            or type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0
            or type(max_bytes) is not int or max_bytes < 1):
        raise ValueError("Command, positive timeout and output limit are required")
    if len(prompt.encode("utf-8")) > max_bytes:
        raise ValueError("Prompt exceeds input limit")
    child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    output = [bytearray(), bytearray()]
    exceeded = threading.Event()
    stream_error = threading.Event()
    incomplete = False

    def terminate():
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except PermissionError:
            stream_error.set()
            try:
                child.kill()
            except ProcessLookupError:
                pass
            except OSError:
                stream_error.set()

    def drain(pipe, buffer):
        try:
            while True:
                data = pipe.read(65536)
                if not data:
                    break
                remaining = max_bytes - len(buffer)
                buffer.extend(data[:max(0, remaining)])
                if len(data) > remaining:
                    exceeded.set()
                    terminate()
        except OSError:
            stream_error.set()
            terminate()
        finally:
            pipe.close()

    def send():
        try:
            child.stdin.write(prompt.encode("utf-8"))
            child.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        finally:
            child.stdin.close()

    threads = [threading.Thread(target=drain, args=(p, b), daemon=True)
               for p, b in zip((child.stdout, child.stderr), output)]
    threads.append(threading.Thread(target=send, daemon=True))
    for thread in threads:
        thread.start()
    try:
        child.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        terminate()
        child.wait(timeout=5)
        raise ValueError("Provider timed out; no output was accepted") from None
    except BaseException:
        terminate()
        child.wait(timeout=5)
        raise
    finally:
        for thread in threads:
            thread.join(timeout=2)
        if any(t.is_alive() for t in threads):
            incomplete = True
            terminate()
            for thread in threads:
                thread.join(timeout=2)
    if incomplete:
        raise ValueError("Provider streams did not close; no partial output was accepted")
    if exceeded.is_set():
        raise ValueError("Provider exceeded output limit")
    if stream_error.is_set():
        raise ValueError("Provider stream or cleanup failed; no output was accepted")
    if child.returncode:
        raise ValueError(f"Provider exited {child.returncode}; no output was accepted")
    try:
        return bytes(output[0]).decode("utf-8")
    except UnicodeError:
        raise ValueError("Provider stdout is not UTF-8") from None
