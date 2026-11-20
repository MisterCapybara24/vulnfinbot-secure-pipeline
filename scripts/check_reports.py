import json
from pathlib import Path

names = ["bandit-report.json", "semgrep-report.json", "dependency-report.json", "trivy-report.json", "zap-report.json", "ai-security-report.md"]
for name in names:
    path = Path("reports") / name
    assert path.is_file() and path.stat().st_size > 0, f"Missing or empty report: {name}"
    if path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8-sig"))
    else:
        assert "real Ollama" in path.read_text(encoding="utf-8"), "Real AI evidence required"
    print(f"OK {name}")
