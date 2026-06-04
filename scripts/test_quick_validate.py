import subprocess, sys, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent

def run():
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "quick_validate.py")],
        capture_output=True, text=True
    )

def test_passes_on_clean_repo():
    result = run()
    assert result.returncode == 0, f"expected pass, got:\n{result.stdout}\n{result.stderr}"
    assert "All checks passed" in result.stdout

if __name__ == "__main__":
    test_passes_on_clean_repo()
    print("test_quick_validate: PASS")
