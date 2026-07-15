import json, subprocess, sys
from pathlib import Path
SCRIPT = Path(__file__).resolve().parent / "canary_persona.py"

def _run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

def test_one_persona_per_flow():
    r = _run("checkout,signup,quote", "pii-canary.ab12@inbox.observepoint.com")
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert [p["flow"] for p in out["personas"]] == ["checkout", "signup", "quote"]

def test_subaddress_emails():
    r = _run("checkout,signup", "pii-canary.ab12@inbox.observepoint.com", "--email-mode", "subaddress")
    out = json.loads(r.stdout)
    emails = {p["flow"]: p["email"] for p in out["personas"]}
    assert emails["checkout"] == "pii-canary.ab12+checkout@inbox.observepoint.com"
    assert emails["signup"] == "pii-canary.ab12+signup@inbox.observepoint.com"

def test_shared_emails_all_use_base():
    r = _run("checkout,signup", "pii-canary.ab12@inbox.observepoint.com", "--email-mode", "shared")
    out = json.loads(r.stdout)
    assert {p["email"] for p in out["personas"]} == {"pii-canary.ab12@inbox.observepoint.com"}

def test_uniqueness_after_normalization():
    r = _run("checkout,signup,quote,login", "pii-canary.ab12@inbox.observepoint.com")
    out = json.loads(r.stdout)
    ps = out["personas"]
    # names, phone digits, addresses, accountIds distinct across flows (post-normalization)
    assert len({p["name"].strip().lower() for p in ps}) == len(ps)
    assert len({"".join(c for c in p["phone"] if c.isdigit()) for p in ps}) == len(ps)
    assert len({p["accountId"] for p in ps}) == len(ps)

def test_determinism_under_seed():
    a = _run("checkout,signup", "b@x.com", "--seed", "7").stdout
    b = _run("checkout,signup", "b@x.com", "--seed", "7").stdout
    assert a == b
    c = _run("checkout,signup", "b@x.com", "--seed", "8").stdout
    assert a != c  # different seed → different personas

def test_e164_phone_shape():
    r = _run("checkout", "b@x.com")
    p = json.loads(r.stdout)["personas"][0]
    assert p["phone"].startswith("+1") and "555" in p["phone"]

def test_bad_input_errors():
    assert _run().returncode != 0                      # no args
    assert _run("checkout", "notanemail").returncode != 0  # base missing @

def test_too_many_flows_errors():
    flows = ",".join(f"f{i}" for i in range(50))
    r = _run(flows, "b@x.com")
    assert r.returncode != 0
    assert "too many flows" in (r.stdout + r.stderr).lower()

if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print(f"{name}: PASS")
    print("test_canary_persona: ALL PASS")
