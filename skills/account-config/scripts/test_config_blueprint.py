import json, subprocess, sys
from pathlib import Path
SCRIPT = Path(__file__).resolve().parent / "config_blueprint.py"

def _run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

def test_ccpa_blueprint_has_three_audits():
    r = _run("ccpa")
    assert r.returncode == 0, r.stderr
    bp = json.loads(r.stdout)
    assert bp["regulation"] == "ccpa"
    names = [a["name"] for a in bp["audits"]]
    assert len(bp["audits"]) == 3
    assert any("opt-out" in n.lower() for n in names)
    assert any("gpc" in n.lower() for n in names)

def test_unknown_regulation_errors():
    r = _run("zzznope")
    assert r.returncode != 0
    assert "unknown regulation" in (r.stdout + r.stderr).lower()

if __name__ == "__main__":
    test_ccpa_blueprint_has_three_audits()
    test_unknown_regulation_errors()
    print("test_config_blueprint: PASS")
