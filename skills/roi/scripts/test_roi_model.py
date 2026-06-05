import json, subprocess, sys
from pathlib import Path
SCRIPT = Path(__file__).resolve().parent / "roi_model.py"

def test_sums_value_categories():
    inp = json.dumps({
        "incidents_caught": 4, "avg_incident_cost": 50000,
        "manual_qa_hours_saved": 200, "hourly_rate": 75,
        "wasted_adspend_reduced": 120000,
    })
    r = subprocess.run([sys.executable, str(SCRIPT)], input=inp, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["total_estimated_value"] == 335000
    assert "incident_avoidance" in out["categories"]
    assert out["disclaimer"].lower().startswith("value framing")

if __name__ == "__main__":
    test_sums_value_categories()
    print("test_roi_model: PASS")
