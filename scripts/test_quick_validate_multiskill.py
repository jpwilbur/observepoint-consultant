"""Multi-skill resolution tests for quick_validate, using a temp fixture tree."""
import subprocess, sys, tempfile
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parent / "quick_validate.py"

FRONT = "---\nname: {name}\ndescription: d\n---\n\n# {name}\n\n{body}\n"
FOOTER = "\n*Last verified: 2026-06-04*\n"

def _write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

def _make_repo(root: Path):
    _write(root / ".claude-plugin/plugin.json", '{"name":"x","description":"d","author":{"name":"a","email":"e"}}')
    _write(root / ".claude-plugin/marketplace.json", '{"name":"x","description":"d","owner":{"name":"a","email":"e"},"plugins":[]}')
    _write(root / "skills/observepoint-consultant/SKILL.md", FRONT.format(name="observepoint-consultant", body="see references/mcp-tools.md"))
    _write(root / "skills/observepoint-consultant/references/mcp-tools.md", "# mcp tools" + FOOTER)
    _write(root / "skills/regulation/SKILL.md", FRONT.format(name="regulation", body="uses references/mcp-tools.md and references/privacy.md"))
    _write(root / "skills/regulation/references/privacy.md", "# privacy" + FOOTER)

def test_multiskill_clean_passes():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        (root / "scripts/quick_validate.py").write_text(VALIDATOR.read_text())
        _make_repo(root)
        r = subprocess.run([sys.executable, str(root / "scripts/quick_validate.py")], cwd=root, capture_output=True, text=True)
        assert r.returncode == 0, f"expected pass:\n{r.stdout}\n{r.stderr}"
        assert "All checks passed" in r.stdout

def test_multiskill_broken_ref_fails():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        (root / "scripts/quick_validate.py").write_text(VALIDATOR.read_text())
        _make_repo(root)
        p = root / "skills/regulation/SKILL.md"
        p.write_text(p.read_text() + "\nbroken references/does-not-exist.md\n")
        r = subprocess.run([sys.executable, str(root / "scripts/quick_validate.py")], cwd=root, capture_output=True, text=True)
        assert r.returncode == 1, f"expected fail:\n{r.stdout}"
        assert "does-not-exist.md" in r.stdout

def test_missing_footer_fails():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        (root / "scripts/quick_validate.py").write_text(VALIDATOR.read_text())
        _make_repo(root)
        (root / "skills/regulation/references/privacy.md").write_text("# privacy no footer")
        r = subprocess.run([sys.executable, str(root / "scripts/quick_validate.py")], cwd=root, capture_output=True, text=True)
        assert r.returncode == 1
        assert "Last verified" in r.stdout

if __name__ == "__main__":
    test_multiskill_clean_passes()
    test_multiskill_broken_ref_fails()
    test_missing_footer_fails()
    print("test_quick_validate_multiskill: PASS")
