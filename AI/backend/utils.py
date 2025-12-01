import subprocess
import tempfile
import os
import difflib
from typing import Tuple

def apply_patch_to_file(patch_text: str) -> dict:
    # Expects a unified diff patch. This will try to apply patch safely using python
    # For simplicity, write patch to temp file and use 'git apply' if available.
    try:
        import git
    except Exception:
        git = None

    # attempt git apply
    try:
        tmp_patch = tempfile.NamedTemporaryFile(delete=False, suffix=".patch")
        tmp_patch.write(patch_text.encode('utf-8'))
        tmp_patch.flush()
        tmp_patch.close()
        if git:
            repo = git.Repo('.', search_parent_directories=True)
            cmd = ['git', 'apply', tmp_patch.name]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(tmp_patch.name)
            if proc.returncode == 0:
                return {"ok": True, "method": "git apply"}
            else:
                return {"ok": False, "error": proc.stderr}
        else:
            # fallback: attempt naive patch apply (not robust)
            os.unlink(tmp_patch.name)
            return {"ok": False, "error": "gitpython not installed; install gitpython or use git in PATH"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def run_shell_command(cmd: str) -> dict:
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    except Exception as e:
        return {"error": str(e)}
