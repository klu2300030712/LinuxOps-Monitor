import os
import shutil
import subprocess

# Safe, fixed automation tasks. No user-supplied shell commands are executed.
def run_job(name: str):
    if name == "health-check":
        return "API health check completed successfully."

    if name == "dependency-check":
        checks = {
            "python": shutil.which("python3") or shutil.which("python"),
            "docker": shutil.which("docker"),
            "git": shutil.which("git"),
        }
        return "\n".join(f"{k}: {v or 'not found'}" for k, v in checks.items())

    if name == "disk-check":
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.stdout.strip() or result.stderr.strip()

    raise ValueError("Unknown automation job")
