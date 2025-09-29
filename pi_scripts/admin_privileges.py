#!/usr/bin/env python3
"""
Auto-elevation helper (Windows UAC + Linux sudo)

Folosește-l la începutul scriptului tău pentru a te relansa automat cu privilegii
dacă nu rulezi deja ca admin/root.

Ex:
    from elevate_runner import ensure_elevated
    ensure_elevated()
    # restul codului tău rulează cu privilegii

Dacă vrei să păstrezi totul într-un singur fișier, copiază funcția ensure_elevated() în scan.py
și apeleaz-o imediat.
"""

import os
import sys
import platform

def is_windows():
    return platform.system().lower() == "windows"

# --- Windows helpers ---
def is_admin_windows():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def elevate_windows():
    """
    Relaunch current script with UAC prompt (runas).
    """
    import ctypes
    # cale absolută către python interpreter și script
    python_exe = sys.executable
    script = os.path.abspath(sys.argv[0])

    # construim argumentele (script + rest)
    # Le punem între ghilimele ca să suportăm spații în path
    args = [f'"{script}"'] + [f'"{arg}"' for arg in sys.argv[1:]]
    params = " ".join(args)

    # ShellExecuteW: hwnd, verb, file, params, cwd, show
    try:
        # runas => triggers UAC
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, params, None, 1)
        # ret > 32 => success, otherwise error code
        if int(ret) <= 32:
            raise RuntimeError(f"ShellExecuteW failed, return code: {ret}")
    except Exception as e:
        print("Eroare la elevarea pe Windows:", e, file=sys.stderr)
        sys.exit(1)

# --- Linux helpers ---
def is_root_linux():
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Platform without geteuid (e.g. Windows) -> not root
        return False

def elevate_linux():
    """
    Relaunch current script with sudo preserving argv.
    Folosește os.execvp pentru a înlocui procesul curent.
    """
    python_exe = sys.executable
    args = ['sudo', python_exe] + sys.argv
    try:
        os.execvp('sudo', args)
    except Exception as e:
        print("Eroare la elevarea pe Linux (sudo):", e, file=sys.stderr)
        sys.exit(1)

# --- Public function ---
def ensure_elevated():
    """
    Verifică dacă procesul curent are privilegii. Dacă nu, se relansează cu ele
    (Windows -> UAC, Linux -> sudo). După apel, dacă nu era elevat, procesul
    original se încheie și scriptul rulează în procesul elevat.
    """
    if is_windows():
        if is_admin_windows():
            # deja admin
            return
        else:
            # relansează cu UAC
            elevate_windows()
            # după apelul la ShellExecuteW, scriptul original trebuie să iasă
            # pentru a nu continua în procesul ne-elevat
            sys.exit(0)
    else:
        # presupunem Linux/Unix
        if is_root_linux():
            return
        else:
            # relansează cu sudo
            elevate_linux()
            # os.execvp nu ar trebui să revină; dacă revine, închidem
            sys.exit(0)

# --- test quick run (optional) ---
if __name__ == "__main__":
    print("Înainte de ensure_elevated: uid/gid / is_admin ->", end=" ")
    if is_windows():
        print("Windows, is_admin:", is_admin_windows())
    else:
        try:
            print("Linux, euid:", os.geteuid())
        except Exception:
            print("Non-Linux platform")

    ensure_elevated()

    # codul de mai jos rulează doar după ce avem privilegii
    print("Acum rulez cu privilegii. UID/GID / is_admin ->", end=" ")
    if is_windows():
        print("Windows, is_admin:", is_admin_windows())
    else:
        try:
            print("Linux, euid:", os.geteuid())
        except Exception:
            print("Non-Linux platform")
    # aici poți pune scanarea ta sau importa funcții și le apela
