"""
SMS Service Manager for Flatopia
- Manages start/stop/restart/status for:
  1) SMS API (api.simple_sms_api:sms_app) on :8001
  2) (Optional) Forward Stub (api.forward_stub:forward_app) on :9000
- Loads environment variables from config/sms.env (KEY=VALUE) if present
- Writes PID files under .run and logs under /tmp
"""
import os
import sys
import time
import signal
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / ".run"
RUN_DIR.mkdir(exist_ok=True)

SMS_PID = RUN_DIR / "sms.pid"
FWD_PID = RUN_DIR / "forward.pid"
WRK_PID = RUN_DIR / "inbound.pid"

SMS_LOG = "/tmp/sms_prod.log"
FWD_LOG = "/tmp/forward_stub.log"

SMS_APP = "api.simple_sms_api:sms_app"
FWD_APP = "api.forward_stub:forward_app"

def load_env_file():
    """Load KEY=VALUE lines from config/sms.env if exists."""
    env_path = ROOT / "config" / "sms.env"
    if env_path.exists():
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

def is_running(pid_file: Path) -> bool:
    try:
        if not pid_file.exists():
            return False
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)
        return True
    except Exception:
        return False

def start_forward():
    if is_running(FWD_PID):
        print("Forward stub already running")
        return
    cmd = [sys.executable, "-m", "uvicorn", FWD_APP, "--host", "0.0.0.0", "--port", "9000"]
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=open(FWD_LOG, "a"), stderr=subprocess.STDOUT)
    FWD_PID.write_text(str(proc.pid))
    time.sleep(1)
    print(f"Started forward stub PID {proc.pid} -> http://localhost:9000")

def start_sms():
    if is_running(SMS_PID):
        print("SMS service already running")
        return
    # Ensure critical env defaults if not set (can be overridden by config)
    os.environ.setdefault("MESSAGEMEDIA_SOURCE_NUMBER", "+61499352828")
    cmd = [sys.executable, "-m", "uvicorn", SMS_APP, "--host", "0.0.0.0", "--port", "8001", "--no-access-log"]
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=open(SMS_LOG, "a"), stderr=subprocess.STDOUT)
    SMS_PID.write_text(str(proc.pid))
    time.sleep(1)
    print(f"Started SMS service PID {proc.pid} -> http://localhost:8001")

def start_inbound_worker():
    if is_running(WRK_PID):
        print("Inbound worker already running")
        return
    cmd = [sys.executable, "api/mm_inbound_worker.py"]
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=open("/tmp/mm_inbound_worker.log", "a"), stderr=subprocess.STDOUT)
    WRK_PID.write_text(str(proc.pid))
    time.sleep(1)
    print(f"Started inbound worker PID {proc.pid}")

def stop_pid(pid_file: Path, name: str):
    if not pid_file.exists():
        print(f"{name} not running")
        return
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        if is_running(pid_file):
            os.kill(pid, signal.SIGKILL)
        pid_file.unlink(missing_ok=True)
        print(f"Stopped {name} (PID {pid})")
    except Exception as e:
        print(f"Failed stopping {name}: {e}")

def status():
    print("Status:")
    print(f"  Forward stub: {'running' if is_running(FWD_PID) else 'stopped'}")
    print(f"  SMS service : {'running' if is_running(SMS_PID) else 'stopped'}")

def main():
    parser = argparse.ArgumentParser(description="Flatopia SMS Service Manager")
    parser.add_argument("action", choices=["start", "stop", "restart", "status"], help="action")
    parser.add_argument("--with-forward", dest="with_forward", action="store_true", help="also manage forward stub")
    parser.add_argument("--with-worker", dest="with_worker", action="store_true", help="also manage inbound worker")
    args = parser.parse_args()

    load_env_file()

    if args.action == "start":
        if args.with_forward:
            start_forward()
        start_sms()
        if args.with_worker:
            start_inbound_worker()
    elif args.action == "stop":
        stop_pid(SMS_PID, "SMS service")
        if args.with_forward:
            stop_pid(FWD_PID, "Forward stub")
        if args.with_worker:
            stop_pid(WRK_PID, "Inbound worker")
    elif args.action == "restart":
        stop_pid(SMS_PID, "SMS service")
        if args.with_forward:
            stop_pid(FWD_PID, "Forward stub")
        if args.with_worker:
            stop_pid(WRK_PID, "Inbound worker")
        time.sleep(1)
        if args.with_forward:
            start_forward()
        start_sms()
        if args.with_worker:
            start_inbound_worker()
    elif args.action == "status":
        status()

if __name__ == "__main__":
    main()


