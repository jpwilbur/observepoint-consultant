import json, subprocess, sys, tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "classify_tag_inventory.py"

def _run(inv):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(inv, f)
        path = f.name
    return subprocess.run([sys.executable, str(SCRIPT), path], capture_output=True, text=True)

def test_classifies_known_categories():
    inv = [
        {"name": "Google Analytics 4", "domain": "google-analytics.com"},
        {"name": "Meta Pixel", "domain": "facebook.net"},
        {"name": "FullStory", "domain": "fullstory.com"},
        {"name": "Acme Internal", "domain": "acme.example"},
    ]
    r = _run(inv)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    by_name = {t["name"]: t for t in out["tags"]}
    assert by_name["Google Analytics 4"]["category"] == "analytics"
    assert by_name["Meta Pixel"]["category"] == "advertising"
    assert by_name["FullStory"]["category"] == "session-replay"
    assert by_name["Acme Internal"]["category"] == "unknown"
    assert by_name["Meta Pixel"]["review"] is True
    assert by_name["FullStory"]["review"] is True
    assert by_name["Acme Internal"]["review"] is True
    assert by_name["Google Analytics 4"]["review"] is False
    assert out["summary"]["review_count"] == 3

if __name__ == "__main__":
    test_classifies_known_categories()
    print("test_classify_tag_inventory: PASS")
