#!/usr/bin/env python3
import os
import sys
import platform
import shutil

# --- Helpers ---
def is_linux():
    return platform.system().lower() == "linux"

def is_root_linux():
    """
    Checks if we are root on Linux. If the platform does not have geteuid,
    returns False.
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def elevate_linux():
    """
    Relaunch current script with sudo preserving argv.
    """
    # check if sudo is available
    if shutil.which("sudo") is None:
        print("[Error] 'sudo' nu este disponibil pe sistem.", file=sys.stderr)
        sys.exit(1)

    python_exe = sys.executable
    args = ['sudo', python_exe] + sys.argv
    try:
        os.execvp('sudo', args)
    except Exception as e:
        print("[Error] Linux (sudo):", e, file=sys.stderr)
        sys.exit(1)

# --- Public function ---
def ensure_elevated():
    """
    On Linux: if we are not root, we restart with sudo.
On Windows (and other platforms): we do nothing, we run normally.
    """
    if is_linux():
        if is_root_linux():
            return
        else:
            # relaunch with sudo (replace current process)
            elevate_linux()
            # os.execvp should not return; if it does, we close
            sys.exit(0)
    else:
        # Windows / macOS / etc. -> nothing to do
        return

# --- test quick run (optional) ---
if __name__ == "__main__":
    print(f"Platform: {platform.system()}")
    if is_linux():
        try:
            print("EUID before:", os.geteuid())
        except Exception:
            print("I couldn't read the EUID.")
    else:
        print("We do not run elevation on this platform..")

    ensure_elevated()

    # This message will only be displayed after we ensure we have privileges (on Linux)
    print("We should have admin privileges now.")
